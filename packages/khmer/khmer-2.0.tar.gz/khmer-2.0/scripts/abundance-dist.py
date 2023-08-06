#! /usr/bin/env python
# This file is part of khmer, https://github.com/dib-lab/khmer/, and is
# Copyright (C) 2010-2015, Michigan State University.
# Copyright (C) 2015, The Regents of the University of California.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#
#     * Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
#     * Neither the name of the Michigan State University nor the names
#       of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written
#       permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Contact: khmer-project@idyll.org
# pylint: disable=missing-docstring
"""
Produce the k-mer abundance distribution for the given file.

% python scripts/abundance-dist.py [ -z -s ] <htname> <data> <histout>

Use '-h' for parameter help.
"""
from __future__ import print_function

import sys
import csv
import khmer
import argparse
import textwrap
import os
from khmer import __version__
from khmer.kfile import check_input_files
from khmer.khmer_args import (info, sanitize_help, ComboFormatter,
                              _VersionStdErrAction)


def get_parser():
    epilog = """\
    Example::

        load-into-countgraph.py -x 1e7 -N 2 -k 17 counts \\
                tests/test-data/test-abund-read-2.fa
        abundance-dist.py counts tests/test-data/test-abund-read-2.fa test-dist
    """
    parser = argparse.ArgumentParser(
        description="Calculate abundance distribution of the k-mers in "
        "the sequence file using a pre-made k-mer countgraph.",
        formatter_class=ComboFormatter, epilog=textwrap.dedent(epilog))

    parser.add_argument('input_count_graph_filename', help='The name of the'
                        ' input k-mer countgraph file.')
    parser.add_argument('input_sequence_filename', help='The name of the input'
                        ' FAST[AQ] sequence file.')
    parser.add_argument('output_histogram_filename', help='The columns are: '
                        '(1) k-mer abundance, (2) k-mer count, (3) cumulative '
                        'count, (4) fraction of total distinct k-mers.')
    parser.add_argument('-z', '--no-zero', dest='output_zero', default=True,
                        action='store_false',
                        help='Do not output zero-count bins')
    parser.add_argument('-s', '--squash', dest='squash_output', default=False,
                        action='store_true',
                        help='Overwrite existing output_histogram_filename')
    parser.add_argument('-b', '--no-bigcount', dest='bigcount', default=True,
                        action='store_false',
                        help='Do not count k-mers past 255')
    parser.add_argument('--version', action=_VersionStdErrAction,
                        version='khmer {v}'.format(v=__version__))
    parser.add_argument('-f', '--force', default=False, action='store_true',
                        help='Continue even if specified input files '
                        'do not exist or are empty.')
    return parser


def main():
    info('abundance-dist.py', ['counting'])
    args = sanitize_help(get_parser()).parse_args()

    infiles = [args.input_count_graph_filename,
               args.input_sequence_filename]
    for infile in infiles:
        check_input_files(infile, False)

    print('Counting graph from', args.input_count_graph_filename,
          file=sys.stderr)
    countgraph = khmer.load_countgraph(
        args.input_count_graph_filename)

    if not countgraph.get_use_bigcount() and args.bigcount:
        print("WARNING: The loaded graph has bigcount DISABLED while bigcount"
              " reporting is ENABLED--counts higher than 255 will not be "
              "reported.",
              file=sys.stderr)

    countgraph.set_use_bigcount(args.bigcount)

    kmer_size = countgraph.ksize()
    hashsizes = countgraph.hashsizes()
    tracking = khmer._Nodegraph(  # pylint: disable=protected-access
        kmer_size, hashsizes)

    print('K:', kmer_size, file=sys.stderr)
    print('outputting to', args.output_histogram_filename, file=sys.stderr)

    if args.output_histogram_filename in ('-', '/dev/stdout'):
        pass
    elif os.path.exists(args.output_histogram_filename):
        if not args.squash_output:
            print('ERROR: %s exists; not squashing.' %
                  args.output_histogram_filename,
                  file=sys.stderr)
            sys.exit(1)

        print('** squashing existing file %s' %
              args.output_histogram_filename, file=sys.stderr)

    print('preparing hist...', file=sys.stderr)
    abundances = countgraph.abundance_distribution(
        args.input_sequence_filename, tracking)
    total = sum(abundances)

    if 0 == total:
        print("ERROR: abundance distribution is uniformly zero; "
              "nothing to report.", file=sys.stderr)
        print("\tPlease verify that the input files are valid.",
              file=sys.stderr)
        sys.exit(1)

    if args.output_histogram_filename in ('-', '/dev/stdout'):
        countgraph_fp = sys.stdout
    else:
        countgraph_fp = open(args.output_histogram_filename, 'w')
    countgraph_fp_csv = csv.writer(countgraph_fp)
    # write headers:
    countgraph_fp_csv.writerow(['abundance', 'count', 'cumulative',
                                'cumulative_fraction'])

    sofar = 0
    for _, i in enumerate(abundances):
        if i == 0 and not args.output_zero:
            continue

        sofar += i
        frac = sofar / float(total)

        countgraph_fp_csv.writerow([_, i, sofar, round(frac, 3)])

        if sofar == total:
            break


if __name__ == '__main__':
    main()

# vim: set ft=python ts=4 sts=4 sw=4 et tw=79:
