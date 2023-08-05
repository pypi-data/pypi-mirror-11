#!/usr/bin/env python

"""
Read files with interactions summary (with or without p-values) and plot
a scatter plot of all against all (in pairs) of number of reads of interaction
in two libraries. The script will also scatter plot the single reads count
(above the diagonal). On the diagonal print the scatter of singles vs
interactions. In addition computes the correlation of these numbers and
plot a heatmap of the correlations.
"""

import sys
import argparse
from pylab import *
from mpl_toolkits.axes_grid1 import ImageGrid
from collections import defaultdict
import csv
from scipy.stats import spearmanr

def process_command_line(argv):
    """
    Return a 2-tuple: (settings object, args list).
    `argv` is a list of arguments, or `None` for ``sys.argv[1:]``.
    """
    if argv is None:
        argv = sys.argv[1:]

    # initialize the parser object, replace the description
    parser = argparse.ArgumentParser(
        description='Plot scatter plots and correlations',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        'counts_files',
        help='A file with two columns, the first is the name of the library'
        ' and the second is the name of the counts file. The third column'
        ' is the counts of the single reads.')
    parser.add_argument(
        'output_head',
        help='Name of output files prefix, two figures will be generated'
        ' _scatters.tif and _heatmap.tif.')
    parser.add_argument(
        '-l', '--seglen', type=int, default=100,
        help='Length of segment for binning, need to be the same as used to '
        'generate the summary files.')

    settings = parser.parse_args(argv)

    return settings

def get_singles_counts(sname, seglen):
    """
    Count the number of single reads in each region, count each row twice
    one as RNA1 and once as RNA2
    Arguments:
    - `sname`: file name
    - `seglen`: length of bin
    """
    counts = defaultdict(int)
    with open(sname) as fin:
        infile = csv.DictReader(fin, delimiter='\t')
        for line in infile:
            r1_reg = (
                line['RNA1 chromosome'],int(line['RNA1 from'])/seglen*seglen,
                line['RNA1 strand'])
            r2_reg = (
                line['RNA2 chromosome'],int(line['RNA2 from'])/seglen*seglen,
                line['RNA2 strand'])
            counts[r1_reg] += int(line['interactions'])
            counts[r1_reg] += int(line['interactions'])
    return counts

def get_regions_counts(fname, seglen):
    """
    Return a double dictionary with the number of reads for each pair of
    regions
    Arguments:
    - `fname`: Name of counts file
    - `seglen`: length of segment
    """
    counts = defaultdict(int)
    seglen=int(seglen)
    with open(fname) as fin:
        infile = csv.DictReader(fin, delimiter='\t')
        for line in infile:
            t_reg = (
                line['RNA1 chromosome'],int(line['RNA1 from'])/seglen*seglen,
                line['RNA1 strand'], 
                line['RNA2 chromosome'],int(line['RNA2 from'])/seglen*seglen,
                line['RNA2 strand'])
            counts[t_reg] = int(line['interactions'])
    return counts


def plot_scatter(chimera, singles, chisum, lorder, figname):
    """
    Plot scatter plots of all against all
    Return the correlation coefficients of all against all
    Arguments:
    - `chimera`: A dictionary of A double dictionaries of counts of interactions
    - `singles`: A dictionary of dictionaries with singles counts
    - `chisum`: A dictionary of dictionaries of sum of chimeric counts per reg
    - `lorder`: A list of library names in printing order
    - `figname`: Save the figure to this file
    """
    def scatit(dname, dname2, grd, i, j, l1, l2, lln):
        """
        scatterplot the specific plot
        """
        lkeys = set(dname[l1].keys()) | set(dname2[l2].keys())
        xvec = []
        yvec = []
        for k in lkeys:
            xvec.append(dname[l1][k]+1)
            yvec.append(dname2[l2][k]+1)
        spr = spearmanr(xvec, yvec)
        grd[i*lln + j].hexbin(xvec, yvec, xscale = 'log', yscale = 'log', bins='log', mincnt=2, gridsize=(50,50))#plot(xvec, yvec, '.', alpha=0.2)
        grd[i*lln + j].text(10, 10e4, "r=%.2f p=%.2g"%(spr[0], spr[1]))
        grd[i*lln + j].set_xlim([1, 10e5])
        grd[i*lln + j].set_ylim([1, 10e5])
        grd[i*lln + j].set_yscale('log')
        grd[i*lln + j].set_xscale('log')
        grd[i*lln + j].set_xticks([10e0, 10e2, 10e4])
        grd[i*lln + j].set_yticks([10e0, 10e2, 10e4])
        grd[i*lln + j].set_ylabel(l1)
        grd[i*lln + j].set_xlabel(l2)
#        tight_layout()
        return spr
    lln = len(lorder)
    corrs = zeros((lln, lln))
    fig = figure(1, (8, 8), 300)
    rcParams.update({'font.size': 8})
#    f, axarr = subplots(lln, lln, sharex=True, sharey=True)
    grid = ImageGrid(fig, 111, # similar to subplot(111)
                     nrows_ncols = (lln, lln), # creates 2x2 grid of axes
                     axes_pad=0.1, # pad between axes in inch.
                     aspect=True
                     )            
    for i, l1 in enumerate(lorder):
        for j, l2 in enumerate(lorder):
            if i>j: # Print singles
                corrs[i, j] = scatit(
                    singles, singles, grid, i, j, l1, l2, lln)[0]
            elif i==j:
                corrs[i, j] =scatit(singles, chisum, grid, i, j, l1, l2, lln)[0]
            else:
                corrs[i, j] = scatit(
                    chimera, chimera, grid, i, j, l1, l2, lln)[0]
            xlabel(l1)
            ylabel(l2)
    savefig(figname)
    return corrs


    



def main(argv=None):
    settings = process_command_line(argv)
    lib_counts = {}
    lib_singles = {}
    lib_counts_sum = {}
    libnames = []
    with open(settings.counts_files) as fin:
        for line in fin:
            lname, fname, singname = line.strip().split()
            libnames.append(lname)
            lib_counts[lname] = get_regions_counts(fname, settings.seglen)
            lib_singles[lname] = get_singles_counts(singname, settings.seglen)
            lib_counts_sum[lname] = get_singles_counts(fname, settings.seglen)
    corrs = plot_scatter(
        lib_counts, lib_singles, lib_counts_sum, libnames,
        "%s_scatters.tif"%settings.output_head)
    # Plot the heatmap of the correlations
    figure()
    pcolor(corrs[::-1])
    xticks(arange(len(libnames))+0.5, libnames)
    yticks(arange(len(libnames))+0.5, libnames[::-1])
    colorbar()
    savefig("%s_heatmap.tif"%settings.output_head)
    return 0        # success

if __name__ == '__main__':
    status = main()
    sys.exit(status)
