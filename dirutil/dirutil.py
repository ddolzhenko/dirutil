# Copyright (c) 2016 Dmitri Dolzhenko

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#-------------------------------------------------------------------------------

"""Utilities (that should be in python)
"""

#-------------------------------------------------------------------------------

__author__ = "Dmitri Dolzhenko"
__email__  = "d.dolzhenko@gmail.com"

#-------------------------------------------------------------------------------

import os
import subprocess
import checksumdir
import shutil
import stat
import unittest
import collections
import tempfile

#-------------------------------------------------------------------------------
# system

def im_on_windows():
    return os.name == 'nt'

#-------------------------------------------------------------------------------
# folders

def init_fs_structure(path, structure):
    '''Creates folder structure in path according dict from parameters
    example:
    istream = open('filename.txt')
    structure = {
        folder_l0_1: {                   #this is a folder because dict inside
            folder_l1_1 : {},            #this is a empty folder inside upper folder
            file_l1_1.txt: 'Hello world!',   #this is file with contents 'Hello world'
            file_l1_2.ext: istream             #this will create a file with contents from file stream
        },
        file_l0_1: some text inside # file on top
    }

    init_fs_structure(structure)
    '''
    assert isinstance(structure, dict)
    with work_dir(path):
        for name, data in structure.items():
            assert data is not None
            if isinstance(data, dict):  # create a folder
                os.mkdir(name)
                init_fs_structure(name, data)
            elif isinstance(data, str): # just a file
                with open(name, 'w') as f:
                    f.write(data)
            else:                       # everything else threated as stream
                with open(name, 'w') as f:
                    f.write(data.read())



def home_dir():
    if im_on_windows():
        return os.environ['USERPROFILE']

    return os.path.expanduser('~')

def checksum(path):
    """Directory sha1 checksum"""
    return checksumdir.dirhash(path, 'sha1')

def split_path_all(path):
    norm = os.path.normpath(path)
    return norm.split(os.sep)

def mktree(path):
    '''Creates not only last folder in path but all
    for mktree('1/2/3')
    will create 1/
                1/2
                1/2/3
    '''
    folders = split_path_all(path)
    for i, folder in enumerate(folders):
        f = os.sep.join(folders[:i+1])
        if not os.path.isdir(f):
            os.mkdir(f)


def rmdir(path):
    """Forced directory remove"""
    def onerror(func, path, exc_info):
        if not os.access(path, os.W_OK):
            os.chmod(path, stat.S_IWUSR)
            func(path)
        else:
            raise

    shutil.rmtree(path, onerror=onerror)


class work_dir(object):
    """change working dir within 'with' context
    Usage:
        with work_dir('otherdir/foo/'):
            print(os.getcwd())
        print(os.getcwd()) # oldone
    """
    def __init__(self, directory):
        assert isinstance(directory, str)
        self._wanted = directory

    @property
    def previous(self):
        return self._previous

    @property
    def current(self):
        return os.getcwd()

    def __enter__(self):
        self._previous = self.current
        os.chdir(self._wanted)
        return self

    def __exit__(self, *args):
        os.chdir(self.previous)
        del self._previous

    def __str__(self):
        return self.current


class temp_work_dir:

    def __enter__(self):
        self._work_dir = work_dir(tempfile.mkdtemp())
        self._work_dir.__enter__()

    def __exit__(self, *args):
        tmp = self._work_dir.current
        self._work_dir.__exit__()
        rmdir(tmp)
        self._work_dir = None

    def __str__(self):
        return str(self._work_dir)


import unittest
class TestCase(unittest.TestCase):

    def test_1(self):

        print(os.getcwd())

        print('-'*100)




        with work_dir('c:\\') as w:
            print(os.getcwd())
            print(w.current)
            print(w.previous)

        print('-'*100)

        print(os.getcwd())
        print(w.current)
