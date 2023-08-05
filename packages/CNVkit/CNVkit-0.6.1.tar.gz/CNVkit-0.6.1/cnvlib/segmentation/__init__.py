"""Segmentation of copy number values."""
from __future__ import absolute_import, division
import math
import os.path

import numpy as np

from .. import core, ngfrills, params
from ..cnarray import CopyNumArray as CNA

from Bio._py3k import StringIO


def do_segmentation(probes_fname, save_dataframe, method, rlibpath=None):
    """Infer copy number segments from the given coverage table."""
    if not os.path.isfile(probes_fname):
        raise ValueError("Not a file: %s" % probes_fname)

    probes = CNA.read(probes_fname)
    if method == 'haar':
        from . import haar
        return haar.segment_haar(probes)

    # Run R to calculate copy number segments (CBS)
    if method == 'cbs':
        rscript = CBS_RSCRIPT
    elif method == 'flasso':
        rscript = FLASSO_RSCRIPT
    else:
        raise ValueError("Unknown method %r" % method)
    if rlibpath:
        rscript = rscript.replace("# libPaths", '.libPaths(c("%s"))' % rlibpath)
    sample_id = core.fbase(probes_fname)
    with ngfrills.temp_write_text(rscript % (probes_fname,
                                             params.NULL_LOG2_COVERAGE / 2,
                                             sample_id)
                                 ) as script_fname:
        seg_out = ngfrills.call_quiet('Rscript', script_fname)

    # Convert R dataframe contents to our standard 'basic' format
    out_data = []
    for row in core.parse_tsv(StringIO(seg_out)):
        if row[0].startswith(('[', '"sample')):
            continue
        start, end = [int(math.ceil(float(val))) for val in row[2:4]]
        chrom = row[1].strip('"')
        nloci = int(row[4])
        mean_cvg = float(row[5])
        name = 'G' if mean_cvg >= 0. else 'L'
        # Save output
        out_data.append((chrom, start, end, name, mean_cvg, nloci))

    seg_pset = CNA.from_rows(sample_id, out_data, extra_keys=('probes',))
    seg_pset.sort()
    if method == 'flasso':
        seg_pset = squash_segments(seg_pset)
    seg_pset = repair_segments(seg_pset, probes)

    if save_dataframe:
        return seg_pset, seg_out
    else:
        return seg_pset


def squash_segments(seg_pset):
    """Combine contiguous segments."""
    curr_chrom = None
    curr_start = None
    curr_end = None
    curr_val = None
    curr_cnt = 0

    squashed_rows = []
    for row in seg_pset:
        if row['chromosome'] == curr_chrom and row['coverage'] == curr_val:
            # Continue the current segment
            curr_end = row['end']
            curr_cnt += 1
        else:
            # Segment break
            # Finish the current segment
            if curr_cnt:
                squashed_rows.append((curr_chrom, curr_start, curr_end,
                                      ('G' if curr_val >= 0. else 'L'),
                                      curr_val, curr_cnt))
            # Start a new segment
            curr_chrom = row['chromosome']
            curr_start = row['start']
            curr_end = row['end']
            curr_val = row['coverage']
            curr_cnt = 1
    # Remainder
    squashed_rows.append((curr_chrom, curr_start, curr_end,
                          ('G' if curr_val >= 0. else 'L'),
                          curr_val, curr_cnt))
    return seg_pset.to_rows(squashed_rows)


def repair_segments(segments, orig_probes):
    """Post-process segmentation output.

    1. Ensure every chromosome has at least one segment.
    2. Ensure first and last segment ends match 1st/last bin ends
       (but keep log2 as-is).
    """
    segments = segments.copy()
    extra_segments = []
    for chrom, subprobes in orig_probes.by_chromosome():
        chr_seg_idx = np.where(segments.chromosome == chrom)[0]
        orig_start = subprobes[0]['start']
        orig_end =  subprobes[-1]['end']
        if len(chr_seg_idx):
            segments[chr_seg_idx[0]]['start'] = orig_start
            segments[chr_seg_idx[-1]]['end'] = orig_end
            # ENH: Recalculate segment means here?
        else:
            null_segment = (chrom, orig_start, orig_end, "_", 0.0, 0)
            extra_segments.append(null_segment)
    if extra_segments:
        segments.merge(segments.to_rows(extra_segments))
    return segments


CBS_RSCRIPT = """\
#!/usr/bin/env Rscript

# Calculate copy number segmentation by CBS.
# Input: log2 coverage data in Nexus 'basic' format
# Output: the CBS data table

# libPaths
library('PSCBS') # Requires: R.utils, R.oo, R.methodsS3

write("Loading probe coverages into a data frame", stderr())
tbl = read.delim("%s")
tbl = tbl[tbl$log2 >= %d,]  # Ignore low-coverage probes
chrom_rle = rle(as.character(tbl$chromosome))
chrom_names = chrom_rle$value
chrom_lengths = chrom_rle$lengths
chrom_ids = rep(1:length(chrom_names), chrom_lengths)
if (is.null(tbl$weight)) {
    cna = data.frame(chromosome=chrom_ids, x=tbl$start, y=tbl$log2)
} else {
    cna = data.frame(chromosome=chrom_ids, x=tbl$start, y=tbl$log2, w=tbl$weight)
}

write("Pre-processing the probe data for segmentation", stderr())
# Find and exclude the centromere of each chromosome
largegaps = findLargeGaps(cna, minLength=1e6)
if (is.null(largegaps)) {
    knownsegs = NULL
} else {
    # Choose the largest gap in each chromosome and only omit that
    rows_to_keep = c()
    for (i in 1:length(chrom_names)) {
        curr_chrom_mask = (largegaps$chromosome == i)
        if (sum(curr_chrom_mask)) {
            best = which(
                curr_chrom_mask &
                (largegaps$length == max(largegaps[curr_chrom_mask,]$length))
            )
            rows_to_keep = c(rows_to_keep, best)
        }
    }
    knownsegs = gapsToSegments(largegaps[rows_to_keep,])
}

write("Segmenting the probe data", stderr())
fit = segmentByCBS(cna, alpha=.0001, undo=1, min.width=2,
                   joinSegments=FALSE, knownSegments=knownsegs, seed=0xA5EED)

write("Setting segment endpoints to original bin start/end positions", stderr())
write("and recalculating segment means with bin weights", stderr())
for (idx in 1:nrow(fit$output)) {
    if (!is.na(fit$segRows$startRow[idx])) {
        start_bin = fit$segRows$startRow[idx]
        end_bin = fit$segRows$endRow[idx]
        fit$output$start[idx] = tbl$start[start_bin]
        fit$output$end[idx] = tbl$end[end_bin]
        fit$output$mean[idx] = weighted.mean(tbl$log2[start_bin:end_bin],
                                             tbl$weight[start_bin:end_bin])
    }
}

write("Restoring the original chromosome names", stderr())
fit$output$sampleName = '%s'
out = na.omit(fit$output) # Copy for lookup in the loop
out2 = na.omit(fit$output) # Copy to modify
for (i in 1:length(chrom_names)) {
    out2[out$chromosome == i,]$chromosome = chrom_names[i]
}

write("Printing the CBS table to standard output", stderr())
write.table(out2, '', sep='\t', row.names=FALSE)
"""


FLASSO_RSCRIPT = """\
#!/usr/bin/env Rscript

# Calculate copy number segmentation by CBS.
# Input: log2 coverage data in Nexus 'basic' format
# Output: the CBS data table

# libPaths
library('cghFLasso')

tbl <- read.delim("%s")
# Ignore low-coverage probes
tbl <- tbl[tbl$log2 >= %d,]
positions <- (tbl$start + tbl$end) * 0.5

write("Segmenting the probe data", stderr())
fit <- cghFLasso(tbl$log2,
                 FDR=0.005)

# Reformat the output table as SEG
outtable <- data.frame(sample="%s",
                       chromosome=tbl$chromosome,
                       start=tbl$start,
                       end=tbl$end,
                       nprobes=1,
                       value=fit$Esti.CopyN)

write("Printing the segment table to standard output", stderr())
write.table(outtable, '', sep='\t', row.names=FALSE)
"""
