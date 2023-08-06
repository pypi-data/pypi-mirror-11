#! /usr/bin/env python
# vim: set fileencoding=utf-8
# This file is part of khmer, https://github.com/dib-lab/khmer/, and is
# Copyright (C) 2013-2015, Michigan State University.
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
"""Setup for khmer project."""

import ez_setup

import os
import sys
from os import listdir as os_listdir
from os.path import join as path_join
import shutil
import subprocess
import tempfile

from setuptools import setup
from setuptools import Extension
from setuptools.command.build_ext import build_ext as _build_ext
from distutils.spawn import spawn
from distutils.sysconfig import get_config_vars
from distutils.dist import Distribution
from distutils.errors import DistutilsPlatformError

import versioneer
ez_setup.use_setuptools(version="3.4.1")

versioneer.VCS = 'git'
versioneer.versionfile_source = 'khmer/_version.py'
versioneer.versionfile_build = 'khmer/_version.py'
versioneer.tag_prefix = 'v'  # tags are like v1.2.0
versioneer.parentdir_prefix = '.'
CMDCLASS = versioneer.get_cmdclass()

# strip out -Wstrict-prototypes; a hack suggested by
# http://stackoverflow.com/a/9740721
# proper fix coming in http://bugs.python.org/issue1222585
# numpy has a "nicer" fix:
# https://github.com/numpy/numpy/blob/master/numpy/distutils/ccompiler.py
OPT = get_config_vars('OPT')[0]
os.environ['OPT'] = " ".join(
    flag for flag in OPT.split() if flag != '-Wstrict-prototypes'
)

# Checking for OpenMP support. Currently clang doesn't work with OpenMP,
# so it needs to be disabled for now.
# This function comes from the yt project:
# https://bitbucket.org/yt_analysis/yt/src/f7c75759e0395861b52d16921d8ce3ad6e36f89f/yt/utilities/lib/setup.py?at=yt


def check_for_openmp():
    """Check for OpenMP support."""
    # Create a temporary directory
    tmpdir = tempfile.mkdtemp()
    curdir = os.getcwd()
    exit_code = 1

    if os.name == 'nt':
        return False

    try:
        os.chdir(tmpdir)

        # Get compiler invocation
        compiler = os.getenv('CC', 'cc')

        # Attempt to compile a test script.
        # See http://openmp.org/wp/openmp-compilers/
        filename = r'test.c'
        file = open(filename, 'wt', 1)
        file.write(
            """
            #include <omp.h>
            #include <stdio.h>
            int main() {
            #pragma omp parallel
            printf("Hello from thread %d, nthreads %d",
                    omp_get_thread_num(), omp_get_num_threads());
            }
            """
        )
        with open(os.devnull, 'w') as fnull:
            exit_code = subprocess.call([compiler, '-fopenmp', filename],
                                        stdout=fnull, stderr=fnull)

        # Clean up
        file.close()
    finally:
        os.chdir(curdir)
        shutil.rmtree(tmpdir)

    return exit_code == 0

# We bundle tested versions of zlib & bzip2. To use the system zlib and bzip2
# change setup.cfg or use the `--libraries z,bz2` parameter which will make our
# custom build_ext command strip out the bundled versions.

ZLIBDIR = 'third-party/zlib'
BZIP2DIR = 'third-party/bzip2'

BUILD_DEPENDS = []
BUILD_DEPENDS.extend(path_join("lib", bn + ".hh") for bn in [
    "khmer", "kmer_hash", "hashtable", "counting", "hashbits", "labelhash",
    "hllcounter", "khmer_exception", "read_aligner", "subset", "read_parsers",
    "traversal"])

SOURCES = ["khmer/_khmer.cc"]
SOURCES.extend(path_join("lib", bn + ".cc") for bn in [
    "read_parsers", "kmer_hash", "hashtable",
    "hashbits", "labelhash", "counting", "subset", "read_aligner",
    "hllcounter", "traversal"])

SOURCES.extend(path_join("third-party", "smhasher", bn + ".cc") for bn in [
    "MurmurHash3"])

# Don't forget to update lib/Makefile with these flags!
EXTRA_COMPILE_ARGS = ['-O3', '-std=c++11', '-pedantic']
EXTRA_LINK_ARGS = []

if sys.platform == 'darwin':
    # force 64bit only builds
    EXTRA_COMPILE_ARGS.extend(['-arch', 'x86_64', '-mmacosx-version-min=10.7',
                               '-stdlib=libc++'])

if check_for_openmp():
    EXTRA_COMPILE_ARGS.extend(['-fopenmp'])
    EXTRA_LINK_ARGS.extend(['-fopenmp'])

EXTENSION_MOD_DICT = \
    {
        "sources": SOURCES,
        "extra_compile_args": EXTRA_COMPILE_ARGS,
        "extra_link_args": EXTRA_LINK_ARGS,
        "depends": BUILD_DEPENDS,
        "language": "c++",
        "define_macros": [("VERSION", versioneer.get_version()), ],
    }

EXTENSION_MOD = Extension("khmer._khmer",  # pylint: disable=W0142
                          ** EXTENSION_MOD_DICT)
SCRIPTS = []
SCRIPTS.extend([path_join("scripts", script)
                for script in os_listdir("scripts")
                if script.endswith(".py")])

CLASSIFIERS = [
    "Environment :: Console",
    "Environment :: MacOS X",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: BSD License",
    "Natural Language :: English",
    "Operating System :: POSIX :: Linux",
    "Operating System :: MacOS :: MacOS X",
    "Programming Language :: C++",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Topic :: Scientific/Engineering :: Bio-Informatics",
]
if "-rc" in versioneer.get_version():
    CLASSIFIERS.append("Development Status :: 4 - Beta")
else:
    CLASSIFIERS.append("Development Status :: 5 - Production/Stable")

SETUP_METADATA = \
    {
        "name": "khmer",
        "version": versioneer.get_version(),
        "description": 'khmer k-mer counting library',
        "long_description": open("README.rst").read(),
        "author": "Michael R. Crusoe, Hussien F. Alameldin, Sherine Awad, "
                  "Elmar Bucher, Adam Caldwell, Reed Cartwright, "
                  "Amanda Charbonneau, Bede Constantinides, Greg Edvenson, "
                  "Scott Fay, Jacob Fenton, Thomas Fenzl, Jordan Fish, "
                  "Leonor Garcia-Gutierrez, Phillip Garland, Jonathan Gluck, "
                  "Iván González, Sarah Guermond, Jiarong Guo, Aditi Gupta, "
                  "Joshua R. Herr, Adina Howe, Alex Hyer, Andreas Härpfer, "
                  "Luiz Irber, Rhys Kidd, David Lin, Justin Lippi, "
                  "Tamer Mansour, Pamela McA'Nulty, Eric McDonald, "
                  "Jessica Mizzi, Kevin D. Murray, Joshua R. Nahum, "
                  "Kaben Nanlohy, Alexander Johan Nederbragt, "
                  "Humberto Ortiz-Zuazaga, Jeramia Ory, Jason Pell, "
                  "Charles Pepe-Ranney, Zachary N Russ, Erich Schwarz, "
                  "Camille Scott, Josiah Seaman, Scott Sievert, "
                  "Jared Simpson, Connor T. Skennerton, James Spencer, "
                  "Ramakrishnan Srinivasan, Daniel Standage, "
                  "James A. Stapleton, Joe Stein, Susan R Steinman, "
                  "Benjamin Taylor, Will Trimble, Heather L. Wiencko, "
                  "Michael Wright, Brian Wyss, Qingpeng Zhang, en zyme, "
                  "C. Titus Brown",
        "author_email": 'khmer-project@idyll.org',
        # "maintainer": 'Michael R. Crusoe', # this overrides the author field
        # "maintainer_email": 'mcrusoe@msu.edu', # so don't include it
        # http://docs.python.org/2/distutils/setupscript.html
        # additional-meta-data note #3
        "url": 'https://khmer.readthedocs.org/',
        "packages": ['khmer', 'khmer.tests', 'oxli'],
        "package_dir": {'khmer.tests': 'tests'},
        "install_requires": ['screed >= 0.9', 'bz2file'],
        "extras_require": {':python_version=="2.6"': ['argparse>=1.2.1'],
                           'docs': ['sphinx', 'sphinxcontrib-autoprogram'],
                           'tests': ['nose >= 1.0']},
        "scripts": SCRIPTS,
        # "entry_points": { # Not ready for distribution yet.
        #    'console_scripts': [
        #        "oxli = oxli:main"
        #    ]
        # },
        "ext_modules": [EXTENSION_MOD, ],
        # "platforms": '', # empty as is conveyed by the classifiers below
        # "license": '', # empty as is conveyed by the classifier below
        "include_package_data": True,
        "zip_safe": False,
        "classifiers": CLASSIFIERS
    }


class KhmerBuildExt(_build_ext):  # pylint: disable=R0904

    """Specialized Python extension builder for khmer project.

    Only run the library setup when needed, not on every invocation.

    Also strips out the bundled zlib and bzip2 libraries if
    `--libraries z,bz2` is specified or the equivalent is in setup.cfg
    """

    def run(self):
        """Run extension builder."""
        if "%x" % sys.maxsize != '7fffffffffffffff':
            raise DistutilsPlatformError("%s require 64-bit operating system" %
                                         SETUP_METADATA["packages"])

        if "z" not in self.libraries:
            zcmd = ['bash', '-c', 'cd ' + ZLIBDIR + ' && ( test Makefile -nt'
                    ' configure || bash ./configure --static ) && make -f '
                    'Makefile.pic PIC']
            spawn(cmd=zcmd, dry_run=self.dry_run)
            self.extensions[0].extra_objects.extend(
                path_join("third-party", "zlib", bn + ".lo") for bn in [
                    "adler32", "compress", "crc32", "deflate", "gzclose",
                    "gzlib", "gzread", "gzwrite", "infback", "inffast",
                    "inflate", "inftrees", "trees", "uncompr", "zutil"])
        if "bz2" not in self.libraries:
            bz2cmd = ['bash', '-c', 'cd ' + BZIP2DIR + ' && make -f '
                      'Makefile-libbz2_so all']
            spawn(cmd=bz2cmd, dry_run=self.dry_run)
            self.extensions[0].extra_objects.extend(
                path_join("third-party", "bzip2", bn + ".o") for bn in [
                    "blocksort", "huffman", "crctable", "randtable",
                    "compress", "decompress", "bzlib"])
        _build_ext.run(self)

CMDCLASS.update({'build_ext': KhmerBuildExt})

_DISTUTILS_REINIT = Distribution.reinitialize_command


def reinitialize_command(self, command, reinit_subcommands):
    """Monkeypatch the original version from distutils.

    It's supposed to match the behavior of Distribution.get_command_obj()
    This fixes issues with 'pip install -e' and './setup.py nosetests' not
    respecting the setup.cfg configuration directives for the build_ext
    command.
    """
    cmd_obj = _DISTUTILS_REINIT(self, command, reinit_subcommands)
    options = self.command_options.get(command)
    if options:
        self._set_command_options(  # pylint: disable=protected-access
            cmd_obj, options)
    return cmd_obj
Distribution.reinitialize_command = reinitialize_command


# pylint: disable=W0142
setup(cmdclass=CMDCLASS,
      **SETUP_METADATA)
