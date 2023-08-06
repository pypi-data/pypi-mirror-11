#!python
# This file is part of khmer, https://github.com/dib-lab/khmer/, and is
# Copyright (C) 2011-2015, Michigan State University.
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
# pylint: disable=missing-docstring,invalid-name
"""
Sequence trimming by abundance using countgraph.

Trim sequences at k-mers of the given abundance, based on the given countgraph.
Output sequences will be placed in 'infile.abundfilt'.

% python scripts/filter-abund.py <coungraph> <data1> [ <data2> <...> ]

Use '-h' for parameter help.
"""
from __future__ import print_function
import os
import khmer
import textwrap
import argparse
import sys
from khmer.thread_utils import ThreadedSequenceProcessor, verbose_loader
from khmer.khmer_args import (ComboFormatter, add_threading_args, info,
                              sanitize_help, _VersionStdErrAction)
from khmer.kfile import (check_input_files, check_space,
                         add_output_compression_type, get_file_writer)
from khmer import __version__

DEFAULT_NORMALIZE_LIMIT = 20
DEFAULT_CUTOFF = 2


def get_parser():
    epilog = """\
    Trimmed sequences will be placed in
    ``${input_sequence_filename}.abundfilt`` for each input sequence file. If
    the input sequences are from RNAseq or metagenome sequencing then
    :option:`--variable-coverage` should be used.

    Example::

        load-into-counting.py -k 20 -x 5e7 countgraph data/100k-filtered.fa
        filter-abund.py -C 2 countgraph data/100k-filtered.fa
    """
    parser = argparse.ArgumentParser(
        description='Trim sequences at a minimum k-mer abundance.',
        epilog=textwrap.dedent(epilog),
        formatter_class=ComboFormatter)
    parser.add_argument('input_graph', metavar='input_count_graph_filename',
                        help='The input k-mer countgraph filename')
    parser.add_argument('input_filename', metavar='input_sequence_filename',
                        help='Input FAST[AQ] sequence filename', nargs='+')
    add_threading_args(parser)
    parser.add_argument('--cutoff', '-C', dest='cutoff',
                        default=DEFAULT_CUTOFF, type=int,
                        help="Trim at k-mers below this abundance.")
    parser.add_argument('--variable-coverage', '-V', action='store_true',
                        dest='variable_coverage', default=False,
                        help='Only trim low-abundance k-mers from sequences '
                        'that have high coverage.')
    parser.add_argument('--normalize-to', '-Z', type=int, dest='normalize_to',
                        help='Base the variable-coverage cutoff on this median'
                        ' k-mer abundance.',
                        default=DEFAULT_NORMALIZE_LIMIT)
    parser.add_argument('-o', '--output', dest='single_output_file',
                        type=argparse.FileType('wb'),
                        metavar="optional_output_filename",
                        help='Output the trimmed sequences into a single file '
                        'with the given filename instead of creating a new '
                        'file for each input file.')
    parser.add_argument('--version', action=_VersionStdErrAction,
                        version='khmer {v}'.format(v=__version__))
    parser.add_argument('-f', '--force', default=False, action='store_true',
                        help='Overwrite output file if it exists')
    add_output_compression_type(parser)
    return parser


def main():
    info('filter-abund.py', ['counting'])
    args = sanitize_help(get_parser()).parse_args()

    check_input_files(args.input_graph, args.force)
    infiles = args.input_filename
    if ('-' in infiles or '/dev/stdin' in infiles) and not \
       args.single_output_file:
        print("Accepting input from stdin; output filename must "
              "be provided with -o.", file=sys.stderr)
        sys.exit(1)

    for filename in infiles:
        check_input_files(filename, args.force)

    check_space(infiles, args.force)

    print('loading countgraph:', args.input_graph,
          file=sys.stderr)
    countgraph = khmer.load_countgraph(args.input_graph)
    ksize = countgraph.ksize()

    print("K:", ksize, file=sys.stderr)

    # the filtering function.
    def process_fn(record):
        name = record.name
        seq = record.sequence
        seqN = seq.replace('N', 'A')

        if args.variable_coverage:  # only trim when sequence has high enough C
            med, _, _ = countgraph.get_median_count(seqN)
            if med < args.normalize_to:
                return name, seq

        _, trim_at = countgraph.trim_on_abundance(seqN, args.cutoff)

        if trim_at >= ksize:
            # be sure to not to change the 'N's in the trimmed sequence -
            # so, return 'seq' and not 'seqN'.
            return name, seq[:trim_at]

        return None, None

    if args.single_output_file:
        outfile = args.single_output_file.name
        outfp = get_file_writer(outfile, args.gzip, args.bzip)

    # the filtering loop
    for infile in infiles:
        print('filtering', infile, file=sys.stderr)
        if args.single_output_file:
            outfile = args.single_output_file.name
            outfp = get_file_writer(args.single_output_file, args.gzip,
                                    args.bzip)
        else:
            outfile = os.path.basename(infile) + '.abundfilt'
            outfp = open(outfile, 'wb')
            outfp = get_file_writer(outfp, args.gzip, args.bzip)

        tsp = ThreadedSequenceProcessor(process_fn, n_workers=args.threads)
        tsp.start(verbose_loader(infile), outfp)

        print('output in', outfile, file=sys.stderr)


if __name__ == '__main__':
    main()
