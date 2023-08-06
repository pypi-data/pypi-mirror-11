#!/usr/bin/env python
import setuptools
from distutils.core import setup
import os

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

import whatsmyversion
try:
    git_path = whatsmyversion.find_git_root(os.getcwd())
    __version__ = whatsmyversion.git_describe(git_path, version_prefix='v',
                                              version_suffix='post',
                                              use_local_version_id=False)
except whatsmyversion.NotAGitRepoError:
    __version__ = whatsmyversion.version(whatsmyversion.__file___)

setup(
    name='whatsmyversion',
    version=__version__,
    author='Eric Dill',
    author_email='thedizzle@gmail.com',
    description="Making versioning easy",
    long_description=read('README.rst'),
    py_modules=['whatsmyversion'],
    url='http://github.com/ericdill/whatsmyversion',
    license='GPLv3',
    classifiers = [
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Topic :: Software Development :: Version Control',
    ]
)
