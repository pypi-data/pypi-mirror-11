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
"""Utilities for dealing with multithreaded processing of short reads."""

from __future__ import print_function, unicode_literals

import threading
import sys
import screed
from khmer.utils import write_record, check_is_pair
# stdlib queue module was renamed on Python 3
try:
    import queue
except ImportError:
    import Queue as queue

DEFAULT_WORKER_THREADS = 8
DEFAULT_GROUPSIZE = 100


def verbose_loader(filename):
    """Screed iterator that additionally prints progress info to stderr."""
    screed_iter = screed.open(filename)
    for n, record in enumerate(screed_iter):
        if n % 100000 == 0:
            print('... filtering', n, file=sys.stderr)
        yield record

verbose_fasta_iter = verbose_loader


class SequenceGroup(object):

    def __init__(self, order, seqlist):
        self.order = order
        self.seqlist = seqlist


class ThreadedSequenceProcessor(object):
    QUEUESIZE = 50

    def __init__(self, process_fn, n_workers=DEFAULT_WORKER_THREADS,
                 group_size=DEFAULT_GROUPSIZE, verbose=True):
        self.process_fn = process_fn
        self.n_workers = n_workers
        self.group_size = group_size

        self.inqueue = queue.Queue(self.QUEUESIZE)
        self.outqueue = queue.Queue(self.QUEUESIZE)

        self.worker_count = 0
        self.worker_count_lock = threading.Lock()
        self.done = False
        self.verbose = verbose

        self.n_processed = 0
        self.n_written = 0
        self.bp_processed = 0
        self.bp_written = 0
        self.tallies_lock = threading.Lock()

    def start(self, inputiter, outfp):
        if self.verbose:
            print('starting threads', file=sys.stderr)

        try:
            for _ in range(self.n_workers):
                t = threading.Thread(target=self.do_process)
                self.worker_count += 1
                t.start()

            if self.verbose:
                print('starting writer', file=sys.stderr)

            w = threading.Thread(target=self.do_write, args=(outfp,))
            w.start()

            if self.verbose:
                print('loading...', file=sys.stderr)

            self.push_sequences(inputiter)

            if self.verbose:
                print('done loading in sequences', file=sys.stderr)
            self.done = True

            w.join()
        except Exception:
            self.done = True
            raise

    def push_sequences(self, inputiter):
        batch = []
        last_record = None
        i = 0
        for record in inputiter:
            if i >= self.group_size:
                # keep pairs together in batches, to retain the interleaving.
                if check_is_pair(last_record, record):
                    batch.append(record)
                    g = SequenceGroup(0, batch)
                    self.inqueue.put(g)

                    batch = []
                else:
                    g = SequenceGroup(0, batch)
                    self.inqueue.put(g)
                    batch = [record]

                i = 0
            else:
                batch.append(record)

            last_record = record
            i += 1

        # submit last set of sequences
        if batch:
            g = SequenceGroup(0, batch)
            self.inqueue.put(g)

    def do_process(self):
        inq = self.inqueue

        while not self.done or not inq.empty():
            try:
                g = inq.get(True, 1)
            except queue.Empty:
                continue

            bp_processed = 0
            bp_written = 0

            keep = []
            for record in g.seqlist:
                name, sequence = self.process_fn(record)
                bp_processed += len(record['sequence'])
                if name:
                    quality = record.get('quality')
                    if quality:
                        quality = quality[:len(sequence)]
                    bp_written += len(sequence)
                    keep.append((name, sequence, quality))

            self.outqueue.put(SequenceGroup(0, keep))

            # the tallies are shared among workers, hence we lock
            with self.tallies_lock:

                self.n_processed += len(g.seqlist)
                self.n_written += len(keep)
                self.bp_processed += bp_processed
                self.bp_written += bp_written

                if self.verbose and self.n_processed % 500000 == 0:
                    print("processed %d / wrote %d / removed %d" %
                          (self.n_processed, self.n_written,
                           self.n_processed - self.n_written), file=sys.stderr)
                    print("processed %d bp / wrote %d bp / removed %d bp" %
                          (self.bp_processed, self.bp_written,
                           self.bp_processed - self.bp_written),
                          file=sys.stderr)
                    discarded = self.bp_processed - self.bp_written
                    f = float(discarded) / float(self.bp_processed) * 100
                    print("discarded %.1f%%" % f, file=sys.stderr)

        # end of thread; exit, decrement worker count.
        with self.worker_count_lock:
            self.worker_count -= 1

    def do_write(self, outfp):
        outq = self.outqueue
        while self.worker_count > 0 or not outq.empty():
            try:
                g = outq.get(True, 1)
            except queue.Empty:
                continue

            for name, seq, qual in g.seqlist:
                if qual:
                    record = screed.Record(name=name, sequence=seq,
                                           quality=qual)
                else:
                    record = screed.Record(name=name, sequence=seq)
                write_record(record, outfp)

        if self.verbose:
            print("DONE writing.\nprocessed %d / wrote %d / removed %d" %
                  (self.n_processed, self.n_written,
                   self.n_processed - self.n_written), file=sys.stderr)
            print("processed %d bp / wrote %d bp / removed %d bp" %
                  (self.bp_processed, self.bp_written,
                   self.bp_processed - self.bp_written), file=sys.stderr)
            discarded = self.bp_processed - self.bp_written
            f = float(discarded) / float(self.bp_processed) * 100
            print("discarded %.1f%%" % f, file=sys.stderr)

# vim: set ft=python ts=4 sts=4 sw=4 et tw=79:
