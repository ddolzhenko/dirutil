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

"""Checksums for files and directories
"""

#-------------------------------------------------------------------------------

__author__ = "Dmitri Dolzhenko"
__email__  = "d.dolzhenko@gmail.com"

#-------------------------------------------------------------------------------

import os, hashlib

#-------------------------------------------------------------------------------

md5     = hashlib.md5
sha1    = hashlib.sha1
sha256  = hashlib.sha256
sha512  = hashlib.sha512


def is_hiddden(path):
    return bool(re.search(r'/\.', path))

def walk_if(path, predicate=lambda x: True):
    for x in os.walk(path, topdown=True):
        if predicate(x):
            yield x



def hash_fs(path, hash_algo=sha1):
    if os.path.isdir(path):
        return hash_dir(path, hash_algo)
    elif os.path.isfile(path):
        return hash_file(path, hash_algo)

    raise Exception('{} is not dir and not file'.format(path))


def hash_path(path, hash_algo=sha1):
    hasher = hash_algo()
    hasher.update(path.encode('utf-16').replace('\\', '/'))
    return hasher.hexdigest


def hash_dir(path, hash_algo=sha1):

    hasher = hash_algo()
    for root, dirs, files in os.walk(path, topdown=True):

        in_empty_folder = not dirs and not files

        if in_empty_folder:
            hasher.update(hash_path(root, hash_algo))
        else:
            filenames = (os.path.join(root, f) for f in files)
            hashes = (hash_file(name, hash_algo, consider_filename=True) for name in filenames)
            map(hasher.update, hashes)

    return hasher.hexdigest()



def file_blocks(f, blocksize=1024):
    while True:
        data = f.read(blocksize)
        if not data:
            break
        yield data


def hash_file(filename, hash_algo=sha1, consider_filename=False):
    hasher = hash_algo()

    if consider_filename:
        hasher.update(filename.encode('utf-16'))

    with open(filename, 'rb') as f:
        for data in file_blocks(f, blocksize=1024*64):
            hasher.update(data)

    return hasher.hexdigest()



import unittest

class TestCase(unittest.TestCase):

    def test_1(self):
        folder = "C:\\Users\\Dmitry\\Documents\\repos\\TestGit\\test"

        for x in walk_if(folder):
            print (x)
