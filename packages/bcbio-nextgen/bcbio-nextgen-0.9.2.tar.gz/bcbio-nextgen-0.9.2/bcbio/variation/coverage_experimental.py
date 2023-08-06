import os
import pandas as pd
import subprocess
from collections import Counter

import numpy as np
import math
import pysam
import pybedtools

from bcbio.utils import (file_exists, tmpfile, chdir, splitext_plus,
                         max_command_length, robust_partition_all)
from bcbio.provenance import do
from bcbio.distributed.transaction import file_transaction
from bcbio.log import logger
from bcbio.pipeline import datadict as dd
from bcbio import broad
from bcbio.pipeline import config_utils


class cov_class:

    def __init__(self, size, name, sample):
        self.size = int(size)
        self.name = name
        self.position = ""
        self.sample = sample
        self.cov = {'4': 0, '10': 0, '20': 0, '50': 0}
        self.total = Counter()
        self.raw = 0

    def update(self, size):
        self.size += size

    def save(self, cov, pt):
        self.raw += cov
        self.total[cov] = pt
        for cut in [4, 10, 20, 50]:
            if cov > cut:
                self.cov[str(cut)] += pt

    def save_coverage(self, cov, nt):
        if cov > 100:
            cov = 100
        elif cov > 10:
            cov =  int(math.ceil(cov / 10.0)) * 10
        # self.size += size
        self.total[cov] += nt

    def write_coverage(self, out_file):
        # names = ["region", "size", "sample", "10", "25", "50"]
        df = pd.DataFrame({'depth': self.total.keys(), 'nt': self.total.values()})
        df["size"] = self.size
        df["sample"] = self.sample
        df.to_csv(out_file, mode='a', header=False, index=False, sep="\t")

    def _noise(self):
        m = np.average(map(int, self.total.keys()), weights=self.total.values())
        x = []
        [x.extend([k] * int(float(v) * self.size)) for k, v in self.total.items()]
        sd = np.std(x)
        return m, sd

    def write_regions(self, out_file):
        m, sd = self._noise()
        with open(out_file, 'a') as out_handle:
            print >>out_handle, "\t".join(map(str, [self.position, self.name, self.raw,
                                          "+", self.size, self.sample, m, sd] + self.cov.values()))

def _get_exome_coverage_stats(fn, sample, out_file, total_cov):
    tmp_region = ""
    stats = ""
    with open(fn) as in_handle:
        for line in in_handle:
            if line.startswith("all"):
                continue
            cols = line.strip().split()
            cur_region = "_".join(cols[0:3]) if not isinstance(cols[3], str) else "_".join(cols[0:4])
            if cur_region != tmp_region:
                if tmp_region != "":
                    stats.write_regions(out_file)
                stats = cov_class(cols[-2], cur_region, sample)
                stats.position = "\t".join(cols[0:3])
            stats.save(int(cols[-4]), float(cols[-1]))
            total_cov.save_coverage(int(cols[-4]), int(cols[-3]))
            tmp_region = cur_region
        total_cov.update(int(cols[-2]))
        stats.write_regions(out_file)
    return total_cov

def _silence_run(cmd):
    do._do_run(cmd, False)

def coverage(data):
    AVERAGE_REGION_STRING_LENGTH = 100
    bed_file = dd.get_coverage_experimental(data)
    if not bed_file:
        return data

    work_dir = os.path.join(dd.get_work_dir(data), "report", "coverage")
    batch_size = max_command_length() / AVERAGE_REGION_STRING_LENGTH

    with chdir(work_dir):
        in_bam = data['work_bam']
        sample = dd.get_sample_name(data)
        logger.debug("doing coverage for %s" % sample)
        region_bed = pybedtools.BedTool(bed_file)
        parse_file = os.path.join(sample + "_coverage.bed")
        parse_total_file = os.path.join(sample + "_cov_total.tsv")
        if not file_exists(parse_file):
            total_cov = cov_class(0, None, sample)
            with file_transaction(parse_file) as out_tx:
                with open(out_tx, 'w') as out_handle:
                    HEADER = ["#chrom", "start", "end", "region", "reads",
                              "strand", "size", "sample", "mean", "sd", "cutoff10",
                              "cutoff20", "cutoff4", "cutoff50"]
                    out_handle.write("\t".join(HEADER) + "\n")
                with tmpfile() as tx_tmp_file:
                    lcount = 0
                    for chunk in robust_partition_all(batch_size, region_bed):
                        coord_batch = []
                        line_batch = ""
                        for line in chunk:
                            lcount += 1
                            chrom = line.chrom
                            start = max(line.start, 0)
                            end = line.end
                            coords = "%s:%s-%s" % (chrom, start, end)
                            coord_batch.append(coords)
                            line_batch += str(line)
                        if not coord_batch:
                            continue
                        region_file = pybedtools.BedTool(line_batch,
                                                        from_string=True).saveas().fn
                        coord_string = " ".join(coord_batch)
                        cmd = ("samtools view -b {in_bam} {coord_string} | "
                                "bedtools coverage -a {region_file} -b - "
                                "-hist > {tx_tmp_file}")
                        _silence_run(cmd.format(**locals()))
                        total_cov = _get_exome_coverage_stats(os.path.abspath(tx_tmp_file), sample, out_tx, total_cov)
                        logger.debug("Processed %d regions." % lcount)
            total_cov.write_coverage(parse_total_file)
        data['coverage'] = os.path.abspath(parse_file)
        return data

def variants(data):
    if not "vrn_file" in  data:
        return data
    in_vcf = data['vrn_file']
    work_dir = os.path.join(dd.get_work_dir(data), "report", "variants")
    with chdir(work_dir):
        in_bam = data['work_bam']
        ref_file = dd.get_ref_file(data)
        assert ref_file, "Need the reference genome fasta file."
        jvm_opts = broad.get_gatk_framework_opts(data['config'])
        gatk_jar = config_utils.get_program("gatk", data['config'], "dir")
        bed_file = dd.get_variant_regions(data)
        sample = dd.get_sample_name(data)
        in_bam = data["work_bam"]
        cg_file = os.path.join(sample + "_with-gc.vcf.gz")
        parse_file = os.path.join(sample + "_gc-depth-parse.tsv")
        if not file_exists(cg_file):
            with file_transaction(cg_file) as tx_out:
                cmd = ("java -jar {gatk_jar}/GenomeAnalysisTK.jar -T VariantAnnotator -R {ref_file} "
                       "-L {bed_file} -I {in_bam} "
                       "-A GCContent --variant {in_vcf} --out {tx_out}")
                do.run(cmd.format(**locals()), " GC bias for %s" % in_vcf)

        if not file_exists(parse_file):
            with file_transaction(parse_file) as out_tx:
                with open(out_tx, 'w') as out_handle:
                    print >>out_handle, "CG\tdepth\tsample"
                cmd = ("bcftools query -f '[%GC][\\t%DP][\\t%SAMPLE]\\n' -R  {bed_file} {cg_file} >> {out_tx}")
                do.run(cmd.format(**locals()), " query for %s" % in_vcf)
                logger.debug('parsing coverage: %s' % sample)
        # return df
        return data
