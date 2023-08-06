"""Examine and query coverage in sequencing experiments.

Provides estimates of coverage intervals based on callable regions and
stores coverage per regions in a database using Chanjo
(https://github.com/robinandeer/chanjo)
"""
import collections
import os
import sys
import shutil
import glob

import toolz as tz
import yaml
import sqlite3
from pybedtools import BedTool
import pybedtools

from bcbio import utils, bed
from bcbio.bam import ref
from bcbio.distributed.transaction import file_transaction
from bcbio.log import logger
from bcbio.pipeline import datadict as dd
from bcbio.provenance import do
from bcbio.variation import bedutils

def assign_interval(data):
    """Identify coverage based on percent of genome covered and relation to targets.

    Classifies coverage into 3 categories:
      - genome: Full genome coverage
      - regional: Regional coverage, like exome capture, with off-target reads
      - amplicon: Amplication based regional coverage without off-target reads
    """
    genome_cov_thresh = 0.40  # percent of genome covered for whole genome analysis
    offtarget_thresh = 0.10  # percent of offtarget reads required to be capture (not amplification) based
    if not dd.get_coverage_interval(data):
        vrs = dd.get_variant_regions(data)
        callable_file = dd.get_sample_callable(data)
        if vrs:
            seq_size = pybedtools.BedTool(vrs).total_coverage()
        else:
            seq_size = pybedtools.BedTool(callable_file).total_coverage()
        total_size = sum([c.size for c in ref.file_contigs(dd.get_ref_file(data), data["config"])])
        genome_cov_pct = seq_size / float(total_size)
        if genome_cov_pct > genome_cov_thresh:
            cov_interval = "genome"
            offtarget_pct = 0.0
        else:
            offtarget_stat_file = dd.get_offtarget_stats(data)
            if not offtarget_stat_file:
                offtarget_pct = 0.0
            else:
                with open(offtarget_stat_file) as in_handle:
                    stats = yaml.safe_load(in_handle)
                offtarget_pct = stats["offtarget"] / float(stats["mapped"])
            if offtarget_pct > offtarget_thresh:
                cov_interval = "regional"
            else:
                cov_interval = "amplicon"
        logger.info("Assigned coverage as '%s' with %.1f%% genome coverage and %.1f%% offtarget coverage"
                    % (cov_interval, genome_cov_pct * 100.0, offtarget_pct * 100.0))
        data["config"]["algorithm"]["coverage_interval"] = cov_interval
    return data

def summary(items):
    data = items[0]
    cutoff = dd.get_coverage_depth_min(data)
    work_dir = dd.get_work_dir(data)
    out_dir = utils.safe_makedir(os.path.join(work_dir, "coverage"))
    coverage_bed = dd.get_coverage_regions(data)
    priority_bed = dd.get_priority_regions(data)
    batch = _get_group_batch(items)
    assert batch, ("Did not find batch for samples: %s" %
                   ",".join([dd.get_sample_name(x) for x in items]))
    out_file = os.path.join(out_dir, "%s-coverage.db" % batch)
    if not utils.file_exists(out_file):
        if coverage_bed and priority_bed:
            mini_coverage = bed.minimize(coverage_bed).fn
            mini_priority = bed.minimize(priority_bed).fn
            combined_bed = bed.concat([mini_coverage, mini_priority]).fn
            clean_bed = bedutils.clean_file(combined_bed, data) if len(combined_bed) > 0 else combined_bed.fn
            bed_file = _uniquify_bed_names(clean_bed, out_dir, data)
        else:
            bed_file = None
        if bed_file and utils.file_exists(bed_file):
            with file_transaction(data, out_file) as tx_out_file:
                chanjo = os.path.join(os.path.dirname(sys.executable), "chanjo")
                cmd = ("{chanjo} --db {tx_out_file} build {bed_file}")
                do.run(cmd.format(**locals()), "Prep chanjo database")
                for data in items:
                    sample = dd.get_sample_name(data)
                    bam_file = data["work_bam"]
                    cmd = ("{chanjo} annotate -s {sample} -g {batch} -c {cutoff} "
                           "{bam_file} {bed_file} | "
                           "{chanjo} --db {tx_out_file} import")
                    do.run(cmd.format(**locals()), "Chanjo coverage", data)
        if bed_file:
            os.remove(bed_file)
    coverage = regions_coverage(out_file, batch, out_dir)
    problem_regions = dd.get_problem_region_dir(data)
    if problem_regions:
        coverage = decorate_problem_regions(coverage, problem_regions)
    out = []
    for data in items:
        if utils.file_exists(out_file):
            data["coverage"] = {"summary": out_file,
                                "all": coverage}
        out.append([data])
    return out

def regions_coverage(chanjo_db, batch_name, out_dir):
    """
    create BED file of coverage of all regions from a Chanjo database
    """
    if not utils.file_exists(chanjo_db):
        return None
    out_file = os.path.join(out_dir, batch_name + "-all-regions.bed.gz")
    if utils.file_exists(out_file):
        return out_file
    conn = sqlite3.connect(chanjo_db)
    c = conn.cursor()
    q = c.execute("SELECT contig, start, end, strand, coverage, completeness, "
                  "sample_id "
                  "FROM interval_data "
                  "JOIN interval ON interval_data.parent_id=interval.id ")
    with file_transaction(out_file) as tx_out_file:
        with open(tx_out_file + ".tmp", "w") as out_handle:
            out_handle.write("\t".join(["#chr", "start", "end", "name",
                                       "coverage", "completeness"]) + "\n")
            for line in q:
                line = [str(x) for x in line]
                # chanjo reports coordinates as 1 based instead of 0 based
                start = str(int(line[1]) - 1)
                out_handle.write("\t".join([line[0], start, line[2], line[6],
                                            line[3], line[4], line[5]]) + "\n")
        bt = BedTool(tx_out_file + ".tmp").sort().bgzip()
        shutil.move(bt, tx_out_file)
    return out_file

def _uniquify_bed_names(bed_file, out_dir, data):
    """Chanjo required unique names in the BED file to map to intervals.
    """
    out_file = os.path.join(out_dir, "%s-unames%s" % utils.splitext_plus(os.path.basename(bed_file)))
    if not utils.file_exists(out_file) or not utils.file_uptodate(out_file, bed_file):
        with file_transaction(data, out_file) as tx_out_file:
            with open(bed_file) as in_handle:
                with open(tx_out_file, "w") as out_handle:
                    namecounts = collections.defaultdict(int)
                    for i, line in enumerate(in_handle):
                        parts = line.rstrip("\r\n").split("\t")
                        if len(parts) >= 4:
                            name = parts[3]
                        else:
                            name = str(i)
                        namecount = namecounts.get(name, 0)
                        namecounts[name] += 1
                        if namecount > 0:
                            name = "%s-%s" % (name, namecount)
                        if len(parts) >= 4:
                            parts[3] = name
                        else:
                            assert len(parts) == 3
                            parts.append(name)
                        out_handle.write("\t".join(parts) + "\n")
    return out_file

def _get_group_batch(items):
    out = None
    all_batches = []
    for data in items:
        batches = tz.get_in(("metadata", "batch"), data, [dd.get_sample_name(data)])
        if not isinstance(batches, (list, tuple)):
            batches = [batches]
        batches = [b for b in batches if b]
        all_batches.extend(batches)
        if not out:
            out = set(batches)
        else:
            out = out.intersection(set(batches))
    if len(out) > 0:
        return out.pop()
    else:
        return all_batches[0]

def _handle_multi_batches(prepped, multi_batches):
    """Avoid carrying items present in multiple batches along in analysis.
    """
    out = []
    handled = set([])
    for data in (x[0] for x in prepped):
        name = dd.get_sample_name(data)
        if name in multi_batches:
            if name not in handled:
                out.append([data])
                handled.add(name)
            multi_batches.remove(name)
        elif name not in handled:
            out.append([data])
    assert len(multi_batches) == 0, "Did not find all multi_batch items: %s" % (list(multi_batches))
    return out

def _needs_coverage(data):
    return dd.get_coverage_regions(data) or dd.get_priority_regions(data)

def summarize_samples(samples, run_parallel):
    """Back compatibility for existing pipelines. Should be replaced with summary when ready.
    """
    extras = []
    to_run = collections.defaultdict(list)
    multi_batches = set([])
    for data in [x[0] for x in samples]:
        if _needs_coverage(data):
            sample_name = dd.get_sample_name(data)
            batches = tz.get_in(("metadata", "batch"), data, sample_name)
            if not isinstance(batches, (tuple, list)):
                batches = [batches]
            else:
                multi_batches.add(dd.get_sample_name(data))
            for batch in batches:
                to_run[batch].append(utils.deepish_copy(data))
        else:
            extras.append([data])
    out = run_parallel("coverage_summary", [[xs] for xs in to_run.values()]) if len(to_run) > 0 else []
    out = _handle_multi_batches(out, multi_batches)
    assert len(out + extras) == len(samples), (len(out + extras), len(samples))
    return out + extras

def decorate_problem_regions(query_bed, problem_bed_dir):
    """
    decorate query_bed with percentage covered by BED files of regions specified
    in the problem_bed_dir
    """
    if utils.is_gzipped(query_bed):
        stem, _ = os.path.splitext(query_bed)
        stem, ext = os.path.splitext(stem)
    else:
        stem, ext = os.path.splitext(query_bed)
    out_file = stem + ".problem_annotated" + ext + ".gz"
    if utils.file_exists(out_file):
        return out_file
    bed_files = glob.glob(os.path.join(problem_bed_dir, "*.bed"))
    bed_file_string = " ".join(bed_files)
    names = [os.path.splitext(os.path.basename(x))[0] for x in bed_files]
    names_string = " ".join(names)
    with utils.open_gzipsafe(query_bed) as in_handle:
        header = map(str, in_handle.next().strip().split())
    header = "\t".join(header + names)
    cmd = ("bedtools annotate -i {query_bed} -files {bed_file_string} "
           "-names {names_string} | sed -s 's/^#.*$/{header}/' | bgzip -c > {tx_out_file}")
    with file_transaction(out_file) as tx_out_file:
        message = "Annotate %s with problem regions." % query_bed
        do.run(cmd.format(**locals()), message)
    return out_file
