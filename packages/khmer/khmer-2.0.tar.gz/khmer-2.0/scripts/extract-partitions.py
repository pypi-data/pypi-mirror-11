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
# pylint: disable=invalid-name,missing-docstring
"""
Extract partitioned sequences into files grouped by partition size.

% python scripts/extract-partitions.py <base> <file1.part> [ <file2.part> ... ]

Grouped sequences will be <base>.groupN.fa files.

Use '-h' for parameter help.

@CTB note that if threshold is != 1, those sequences will not be output
by output_unassigned...
"""
from __future__ import print_function

import sys
import screed
import argparse
import textwrap
from khmer import __version__
from khmer.kfile import (check_input_files, check_space,
                         add_output_compression_type,
                         get_file_writer)
from khmer.khmer_args import (info, sanitize_help, ComboFormatter,
                              _VersionStdErrAction)
from khmer.utils import write_record

DEFAULT_MAX_SIZE = int(1e6)
DEFAULT_THRESHOLD = 5


def read_partition_file(filename):
    for record_index, record in enumerate(screed.open(filename)):
        _, partition_id = record.name.rsplit('\t', 1)
        yield record_index, record, int(partition_id)


def get_parser():
    epilog = """\
    Example (results will be in ``example.group0000.fa``)::

        load-graph.py -k 20 example tests/test-data/random-20-a.fa
        partition-graph.py example
        merge-partitions.py -k 20 example
        annotate-partitions.py -k 20 example tests/test-data/random-20-a.fa
        extract-partitions.py example random-20-a.fa.part

    (:program:`extract-partitions.py` will produce a partition size
    distribution in <base>.dist. The columns are: (1) number of reads,
    (2) count of partitions with n reads, (3) cumulative sum of partitions,
    (4) cumulative sum of reads.)
    """
    parser = argparse.ArgumentParser(
        description="Separate sequences that are annotated with partitions "
        "into grouped files.", epilog=textwrap.dedent(epilog),
        formatter_class=ComboFormatter)
    parser.add_argument('prefix', metavar='output_filename_prefix')
    parser.add_argument('part_filenames', metavar='input_partition_filename',
                        nargs='+')
    parser.add_argument('--max-size', '-X', dest='max_size',
                        default=DEFAULT_MAX_SIZE, type=int,
                        help='Max group size (n sequences)')
    parser.add_argument('--min-partition-size', '-m', dest='min_part_size',
                        default=DEFAULT_THRESHOLD, type=int,
                        help='Minimum partition size worth keeping')
    parser.add_argument('--no-output-groups', '-n', dest='output_groups',
                        default=True, action='store_false',
                        help='Do not actually output groups files.')
    parser.add_argument('--output-unassigned', '-U', default=False,
                        action='store_true',
                        help='Output unassigned sequences, too')
    parser.add_argument('--version', action=_VersionStdErrAction,
                        version='khmer {v}'.format(v=__version__))
    parser.add_argument('-f', '--force', default=False, action='store_true',
                        help='Overwrite output file if it exists')
    add_output_compression_type(parser)
    return parser


# pylint: disable=too-many-statements
def main():  # pylint: disable=too-many-locals,too-many-branches
    info('extract-partitions.py', ['graph'])
    args = sanitize_help(get_parser()).parse_args()

    distfilename = args.prefix + '.dist'

    n_unassigned = 0

    for infile in args.part_filenames:
        check_input_files(infile, args.force)

    check_space(args.part_filenames, args.force)

    print('---', file=sys.stderr)
    print('reading partitioned files:', repr(
        args.part_filenames), file=sys.stderr)
    if args.output_groups:
        print('outputting to files named "%s.groupN.fa"' %
              args.prefix, file=sys.stderr)
        print('min reads to keep a partition:',
              args.min_part_size, file=sys.stderr)
        print('max size of a group file:', args.max_size, file=sys.stderr)
    else:
        print('NOT outputting groups! Beware!', file=sys.stderr)

    if args.output_unassigned:
        print('outputting unassigned reads to "%s.unassigned.fa"' %
              args.prefix, file=sys.stderr)
    print('partition size distribution will go to %s'
          % distfilename, file=sys.stderr)
    print('---', file=sys.stderr)

    #

    suffix = 'fa'
    is_fastq = False

    for index, read, pid in read_partition_file(args.part_filenames[0]):
        if hasattr(read, 'quality'):
            suffix = 'fq'
            is_fastq = True
        break

    for filename in args.part_filenames:
        for index, read, pid in read_partition_file(filename):
            if is_fastq:
                assert hasattr(read, 'quality'), \
                    "all input files must be FASTQ if the first one is"
            else:
                assert not hasattr(read, 'quality'), \
                    "all input files must be FASTA if the first one is"

            break

    if args.output_unassigned:
        ofile = open('%s.unassigned.%s' % (args.prefix, suffix), 'wb')
        unassigned_fp = get_file_writer(ofile, args.gzip, args.bzip)
    count = {}
    for filename in args.part_filenames:
        for index, read, pid in read_partition_file(filename):
            if index % 100000 == 0:
                print('...', index, file=sys.stderr)

            count[pid] = count.get(pid, 0) + 1

            if pid == 0:
                n_unassigned += 1
                if args.output_unassigned:
                    write_record(read, unassigned_fp)

    if args.output_unassigned:
        unassigned_fp.close()

    if 0 in count:                          # eliminate unpartitioned sequences
        del count[0]

    # develop histogram of partition sizes
    dist = {}
    for pid, size in list(count.items()):
        dist[size] = dist.get(size, 0) + 1

    # output histogram
    distfp = open(distfilename, 'w')

    total = 0
    wtotal = 0
    for counter, index in sorted(dist.items()):
        total += index
        wtotal += counter * index
        distfp.write('%d %d %d %d\n' % (counter, index, total, wtotal))
    distfp.close()

    if not args.output_groups:
        sys.exit(0)

    # sort groups by size
    divvy = sorted(list(count.items()), key=lambda y: y[1])
    divvy = [y for y in divvy if y[1] > args.min_part_size]

    # divvy up into different groups, based on having max_size sequences
    # in each group.
    total = 0
    group = set()
    group_n = 0
    group_d = {}
    for partition_id, n_reads in divvy:
        group.add(partition_id)
        total += n_reads

        if total > args.max_size:
            for partition_id in group:
                group_d[partition_id] = group_n
                # print 'group_d', partition_id, group_n

            group_n += 1
            group = set()
            total = 0

    if group:
        for partition_id in group:
            group_d[partition_id] = group_n
            # print 'group_d', partition_id, group_n
        group_n += 1

    print('%d groups' % group_n, file=sys.stderr)
    if group_n == 0:
        print('nothing to output; exiting!', file=sys.stderr)
        return

    # open a bunch of output files for the different groups
    group_fps = {}
    for index in range(group_n):
        fname = '%s.group%04d.%s' % (args.prefix, index, suffix)
        group_fp = get_file_writer(open(fname, 'wb'), args.gzip,
                                   args.bzip)
        group_fps[index] = group_fp

    # write 'em all out!

    total_seqs = 0
    part_seqs = 0
    toosmall_parts = 0
    for filename in args.part_filenames:
        for index, read, partition_id in read_partition_file(filename):
            total_seqs += 1
            if index % 100000 == 0:
                print('...x2', index, file=sys.stderr)

            if partition_id == 0:
                continue

            try:
                group_n = group_d[partition_id]
            except KeyError:
                assert count[partition_id] <= args.min_part_size
                toosmall_parts += 1
                continue

            outfp = group_fps[group_n]

            write_record(read, outfp)
            part_seqs += 1

    print('---', file=sys.stderr)
    print('Of %d total seqs,' % total_seqs, file=sys.stderr)
    print('extracted %d partitioned seqs into group files,' %
          part_seqs, file=sys.stderr)
    print('discarded %d sequences from small partitions (see -m),' %
          toosmall_parts, file=sys.stderr)
    print('and found %d unpartitioned sequences (see -U).' %
          n_unassigned, file=sys.stderr)
    print('', file=sys.stderr)
    print('Created %d group files named %s.groupXXXX.%s' %
          (len(group_fps),
           args.prefix,
           suffix), file=sys.stderr)

if __name__ == '__main__':
    main()
