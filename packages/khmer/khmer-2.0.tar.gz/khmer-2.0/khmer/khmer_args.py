# vim: set encoding=utf-8
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

from __future__ import unicode_literals
from __future__ import print_function

import sys
import os
import argparse
import math
import textwrap
from argparse import _VersionAction
from collections import namedtuple

import screed
import khmer
from khmer import extract_countgraph_info, extract_nodegraph_info
from khmer import __version__
from .utils import print_error
from .khmer_logger import log_info, log_warn, configure_logging


DEFAULT_K = 32
DEFAULT_N_TABLES = 4
DEFAULT_MAX_TABLESIZE = 1e6
DEFAULT_N_THREADS = 1


class _VersionStdErrAction(_VersionAction):

    def __call__(self, parser, namespace, values, option_string=None):
        version = self.version
        if version is None:
            version = parser.version
        formatter = parser._get_formatter()
        formatter.add_text(version)
        parser._print_message(formatter.format_help(), sys.stderr)
        parser.exit()


class ComboFormatter(argparse.ArgumentDefaultsHelpFormatter,
                     argparse.RawDescriptionHelpFormatter):
    pass


def optimal_size(num_kmers, mem_cap=None, fp_rate=None):
    """
    Utility function for estimating optimal countgraph args where:
      - num_kmers: number of unique kmers [required]
      - mem_cap: the allotted amount of memory [optional, conflicts with f]
      - fp_rate: the desired false positive rate [optional, conflicts with M]
    """
    if all((num_kmers is not None, mem_cap is not None, fp_rate is None)):
        return estimate_optimal_with_K_and_M(num_kmers, mem_cap)
    elif all((num_kmers is not None, mem_cap is None, fp_rate is not None)):
        return estimate_optimal_with_K_and_f(num_kmers, fp_rate)
    else:
        raise TypeError("num_kmers and either mem_cap or fp_rate"
                        " must be defined.")


def check_conflicting_args(args, hashtype):
    """
    Utility function that takes in an args object and checks if there's things
    that conflict, e.g. --loadgraph and --ksize being set.
    """

    if getattr(args, "quiet", None):
        configure_logging(args.quiet)

    loadgraph_table_conflicts = {"ksize": DEFAULT_K,
                                 "n_tables": DEFAULT_N_TABLES,
                                 "max_tablesize": DEFAULT_MAX_TABLESIZE}

    loadgraph_autoarg_conflicts = ("unique_kmers", "max_memory_usage")

    if getattr(args, "loadgraph", None):

        # check for table config args
        for key, value in loadgraph_table_conflicts.items():
            if getattr(args, key, value) != value:
                log_warn('''
*** WARNING: You are loading a saved k-mer countgraph from
*** {hashfile}, but have set k-mer table parameters.
*** Your values for ksize, n_tables, and tablesize
*** will be ignored.'''.format(hashfile=args.loadgraph))
                break  # no repeat warnings

        for element in loadgraph_autoarg_conflicts:
            if getattr(args, element, None):
                log_warn("\n*** WARNING: You have asked that the graph size be"
                         " automatically calculated\n"
                         "*** (by using -U or -M).\n"
                         "*** But you are loading an existing graph!\n"
                         "*** Size will NOT be set automatically.")
                break  # no repeat warnings

        infoset = None
        if hashtype == 'countgraph':
            infoset = extract_countgraph_info(args.loadgraph)
        if info:
            ksize = infoset[0]
            max_tablesize = infoset[1]
            n_tables = infoset[2]
            args.ksize = ksize
            args.n_tables = n_tables
            args.max_tablesize = max_tablesize


def estimate_optimal_with_K_and_M(num_kmers, mem_cap):
    """
    Utility function for estimating optimal countgraph args where num_kmers
    is the number of unique kmer and mem_cap is the allotted amount of memory
    """

    n_tables = math.log(2) * (mem_cap / float(num_kmers))
    int_n_tables = int(n_tables)
    if int_n_tables == 0:
        int_n_tables = 1
    ht_size = int(mem_cap / int_n_tables)
    mem_cap = ht_size * int_n_tables
    fp_rate = (1 - math.exp(-num_kmers / float(ht_size))) ** int_n_tables
    res = namedtuple("result", ["num_htables", "htable_size", "mem_use",
                                "fp_rate"])
    return res(int_n_tables, ht_size, mem_cap, fp_rate)


def estimate_optimal_with_K_and_f(num_kmers, des_fp_rate):
    """
    Utility function for estimating optimal memory where num_kmers  is the
    number of unique kmers and des_fp_rate is the desired false positive rate
    """
    n_tables = math.log(des_fp_rate, 0.5)
    int_n_tables = int(n_tables)
    if int_n_tables == 0:
        int_n_tables = 1

    ht_size = int(-num_kmers / (
        math.log(1 - des_fp_rate ** (1 / float(int_n_tables)))))
    mem_cap = ht_size * int_n_tables
    fp_rate = (1 - math.exp(-num_kmers / float(ht_size))) ** int_n_tables

    res = namedtuple("result", ["num_htables", "htable_size", "mem_use",
                                "fp_rate"])
    return res(int_n_tables, ht_size, mem_cap, fp_rate)


def graphsize_args_report(unique_kmers, fp_rate):
    """
    Assembles output string for optimal arg sandbox scripts
    takes in unique_kmers and desired fp_rate
    """
    to_print = []

    to_print.append('')  # blank line
    to_print.append('number of unique k-mers: \t{0}'.format(unique_kmers))
    to_print.append('false positive rate: \t{:>.3f}'.format(fp_rate))
    to_print.append('')  # blank line
    to_print.append('If you have expected false positive rate to achieve:')
    to_print.append('expected_fp\tnumber_hashtable(Z)\tsize_hashtable(H)\t'
                    'expected_memory_usage')

    for fp_rate in range(1, 10):
        num_tables, table_size, mem_cap, fp_rate = \
            optimal_size(unique_kmers, fp_rate=fp_rate / 10.0)
        to_print.append('{:11.3f}\t{:19}\t{:17e}\t{:21e}'.format(fp_rate,
                                                                 num_tables,
                                                                 table_size,
                                                                 mem_cap))

    mem_list = [1, 5, 10, 20, 50, 100, 200, 300, 400, 500, 1000, 2000, 5000]

    to_print.append('')  # blank line
    to_print.append('If you have expected memory to use:')
    to_print.append('expected_memory_usage\tnumber_hashtable(Z)\t'
                    'size_hashtable(H)\texpected_fp')

    for mem in mem_list:
        num_tables, table_size, mem_cap, fp_rate =\
            optimal_size(unique_kmers, mem_cap=mem * 1000000000)
        to_print.append('{:21e}\t{:19}\t{:17e}\t{:11.3f}'.format(mem_cap,
                                                                 num_tables,
                                                                 table_size,
                                                                 fp_rate))
    return "\n".join(to_print)


def _check_fp_rate(args, desired_max_fp):
    """
    Function to check if the desired_max_fp rate makes sense given specified
    number of unique kmers and max_memory restrictions present in the args.

    Takes in args object and desired_max_fp
    """
    if not args.unique_kmers:
        return args

    # Do overriding of default script FP rate
    if args.fp_rate:
        log_info("*** INFO: Overriding default fp {def_fp} with new fp:"
                 " {new_fp}", def_fp=desired_max_fp, new_fp=args.fp_rate)
        desired_max_fp = args.fp_rate

    # If we have the info we need to work with, do the stuff
    if args.max_memory_usage:
        # verify that this is a sane memory usage restriction
        res = estimate_optimal_with_K_and_M(args.unique_kmers,
                                            args.max_memory_usage)
        if res.fp_rate > desired_max_fp:
            print("""
*** ERROR: The given restrictions yield an estimate false positive rate of {0},
*** which is above the recommended false positive ceiling of {1}!"""
                  .format(res.fp_rate, desired_max_fp), file=sys.stderr)
            if not args.force:
                print("NOTE: This can be overridden using the --force"
                      " argument", file=sys.stderr)
                print("*** Aborting...!", file=sys.stderr)
                sys.exit(1)
    else:
        res = estimate_optimal_with_K_and_f(args.unique_kmers,
                                            desired_max_fp)
        if args.max_tablesize and args.max_tablesize < res.htable_size:
            log_warn("\n*** Warning: The given tablesize is too small!")
            log_warn("*** Recommended tablesize is: {tsize:5g} bytes",
                     tsize=res.htable_size)
            log_warn("*** Current is: {tsize:5g} bytes",
                     tsize=args.max_tablesize)
            res = estimate_optimal_with_K_and_M(args.unique_kmers,
                                                args.max_tablesize)
            log_warn("*** Estimated FP rate with current config is: {fp}\n",
                     fp=res.fp_rate)
        else:
            if res.mem_use < 1e6:  # one megabyteish
                args.max_memory_usage = 1e6
            else:
                args.max_memory_usage = res.mem_use
            log_info("*** INFO: set memory ceiling automatically.")
            log_info("*** Ceiling is: {ceil:3g} bytes\n",
                     ceil=float(args.max_memory_usage))
            args.max_mem = res.mem_use

    return args


def build_graph_args(descr=None, epilog=None, parser=None):
    """Build an ArgumentParser with args for bloom filter based scripts."""

    if parser is None:
        parser = argparse.ArgumentParser(description=descr, epilog=epilog,
                                         formatter_class=ComboFormatter)

    parser.add_argument('--version', action=_VersionStdErrAction,
                        version='khmer {v}'.format(v=__version__))

    parser.add_argument('--ksize', '-k', type=int, default=DEFAULT_K,
                        help='k-mer size to use')

    parser.add_argument('--n_tables', '-N', type=int,
                        default=DEFAULT_N_TABLES,
                        help='number of tables to use in k-mer countgraph')
    parser.add_argument('-U', '--unique-kmers', type=float, default=0,
                        help='approximate number of unique kmers in the input'
                             ' set')
    parser.add_argument('--fp-rate', type=float, default=None,
                        help="Override the automatic FP rate setting for the"
                        " current script")

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--max-tablesize', '-x', type=float,
                       default=DEFAULT_MAX_TABLESIZE,
                       help='upper bound on tablesize to use; overrides ' +
                       '--max-memory-usage/-M.')
    group.add_argument('-M', '--max-memory-usage', type=float,
                       help='maximum amount of memory to use for data ' +
                       'structure.')

    return parser


def build_counting_args(descr=None, epilog=None):
    """Build an ArgumentParser with args for countgraph based scripts."""
    parser = build_graph_args(descr=descr, epilog=epilog)

    return parser


def build_nodegraph_args(descr=None, epilog=None, parser=None):
    """Build an ArgumentParser with args for nodegraph based scripts."""
    parser = build_graph_args(descr=descr, epilog=epilog, parser=parser)

    return parser

# add an argument for loadgraph with warning about parameters


def add_loadgraph_args(parser):
    parser.add_argument('-l', '--loadgraph', metavar="filename", default=None,
                        help='load a precomputed k-mer graph from disk')


def calculate_graphsize(args, graphtype, multiplier=1.0):
    if graphtype not in ('countgraph', 'nodegraph'):
        raise ValueError("unknown graph type: %s" % (graphtype,))

    if args.max_memory_usage:
        if graphtype == 'countgraph':
            tablesize = args.max_memory_usage / args.n_tables / \
                float(multiplier)
        elif graphtype == 'nodegraph':
            tablesize = 8. * args.max_memory_usage / args.n_tables / \
                float(multiplier)
    else:
        tablesize = args.max_tablesize

    return tablesize


def create_nodegraph(args, ksize=None, multiplier=1.0, fp_rate=0.01):
    """Creates and returns a nodegraph"""
    args = _check_fp_rate(args, fp_rate)
    if ksize is None:
        ksize = args.ksize
    if ksize > 32:
        print_error("\n** ERROR: khmer only supports k-mer sizes <= 32.\n")
        sys.exit(1)

    tablesize = calculate_graphsize(args, 'nodegraph', multiplier)
    return khmer.Nodegraph(ksize, tablesize, args.n_tables)


def create_countgraph(args, ksize=None, multiplier=1.0, fp_rate=0.1):
    """Creates and returns a countgraph"""
    args = _check_fp_rate(args, fp_rate)
    if ksize is None:
        ksize = args.ksize
    if ksize > 32:
        print_error("\n** ERROR: khmer only supports k-mer sizes <= 32.\n")
        sys.exit(1)

    tablesize = calculate_graphsize(args, 'countgraph', multiplier=multiplier)
    return khmer.Countgraph(ksize, tablesize, args.n_tables)


def report_on_config(args, graphtype='countgraph'):
    """Print out configuration.

    Summarize the configuration produced by the command-line arguments
    made available by this module.
    """
    check_conflicting_args(args, graphtype)
    if graphtype not in ('countgraph', 'nodegraph'):
        raise ValueError("unknown graph type: %s" % (graphtype,))

    tablesize = calculate_graphsize(args, graphtype)

    log_info("\nPARAMETERS:")
    log_info(" - kmer size =    {ksize} \t\t(-k)", ksize=args.ksize)
    log_info(" - n tables =     {ntables} \t\t(-N)", ntables=args.n_tables)
    log_info(" - max tablesize = {tsize:5.2g} \t(-x)", tsize=tablesize)
    log_info("")
    if graphtype == 'countgraph':
        log_info(
            "Estimated memory usage is {0:.2g} bytes "
            "(n_tables x max_tablesize)".format(
                args.n_tables * tablesize))
    elif graphtype == 'nodegraph':
        log_info(
            "Estimated memory usage is {0:.2g} bytes "
            "(n_tables x max_tablesize / 8)".format(args.n_tables *
                                                    tablesize / 8)
        )

    log_info("-" * 8)

    if DEFAULT_MAX_TABLESIZE == tablesize and \
       not getattr(args, 'loadgraph', None):
        log_warn('''\

** WARNING: tablesize is default!
** You probably want to increase this with -M/--max-memory-usage!
** Please read the docs!
''')


def add_threading_args(parser):
    """Add option for threading to options parser."""
    parser.add_argument('--threads', '-T', default=DEFAULT_N_THREADS, type=int,
                        help='Number of simultaneous threads to execute')


def sanitize_help(parser):
    """Remove Sphinx directives & reflow text to width of 79 characters."""
    wrapper = textwrap.TextWrapper(width=79)
    parser.description = wrapper.fill(parser.description)
    if not parser.epilog:
        return parser
    cleanlog = parser.epilog.replace(':option:', '').replace(
        ':program:', '').replace('::', ':').replace('``', '"')
    newlog = prev_section = ""
    for section in cleanlog.split('\n\n'):
        if section.startswith('    '):
            newlog += section + '\n'
        else:
            if prev_section.startswith('    '):
                newlog += '\n'
            newlog += wrapper.fill(section) + '\n\n'
        prev_section = section
    parser.epilog = newlog
    return parser

_algorithms = {
    'software': 'MR Crusoe et al., '
    '2015. http://dx.doi.org/10.12688/f1000research.6924.1',
    'diginorm': 'CT Brown et al., arXiv:1203.4802 [q-bio.GN]',
    'streaming': 'Q Zhang, S Awad, CT Brown, '
    'https://dx.doi.org/10.7287/peerj.preprints.890v1',
    'graph': 'J Pell et al., http://dx.doi.org/10.1073/pnas.1121464109',
    'counting': 'Q Zhang et al., '
    'http://dx.doi.org/10.1371/journal.pone.0101271',
    'sweep': 'C Scott, MR Crusoe, and CT Brown, unpublished',
    'SeqAn': 'A. Döring et al. http://dx.doi.org:80/10.1186/1471-2105-9-11',
    'hll': 'Irber and Brown, unpublished'
}


def info(scriptname, algorithm_list=None):
    """Print version and project info to stderr."""
    import khmer

    log_info("\n|| This is the script {name} in khmer.\n"
             "|| You are running khmer version {version}",
             name=scriptname, version=khmer.__version__)
    log_info("|| You are also using screed version {version}\n||",
             version=screed.__version__)

    log_info("|| If you use this script in a publication, please "
             "cite EACH of the following:\n||")

    if algorithm_list is None:
        algorithm_list = []

    algorithm_list.insert(0, 'software')

    for alg in algorithm_list:
        algstr = "||   * " + _algorithms[alg].encode(
            'utf-8', 'surrogateescape').decode('utf-8', 'replace')
        try:
            log_info(algstr)
        except UnicodeEncodeError:
            log_info(algstr.encode(sys.getfilesystemencoding(), 'replace'))

    log_info("||\n|| Please see http://khmer.readthedocs.org/en/"
             "latest/citations.html for details.\n")

# vim: set ft=python ts=4 sts=4 sw=4 et tw=79:
