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

"""
"""

#-------------------------------------------------------------------------------

__author__ = "Dmitri Dolzhenko"
__email__  = "d.dolzhenko@gmail.com"

#-------------------------------------------------------------------------------

import os, stat, shutil, tempfile

class Error:
    pass


#-------------------------------------------------------------------------------
# general
#-------------------------------------------------------------------------------

def split_path(path):
    os.path.normpath(path).split(os.sep)

def exists(path):
    return os.path.exists(path)

def isdir(path):
    return os.isdir(path)

def isfile(path):
    return os.isfile(path)

#-------------------------------------------------------------------------------
# files
#-------------------------------------------------------------------------------

def touch(path):
    with open(path, 'w'):
        pass

def file_write(path, data, mode=''):
    with open(path, 'w' + mode) as f:
        f.write(data)

def file_append(path, data, mode=''):
    with open(path, 'a' + mode) as f:
        f.write(data)


def rmfile(path):
    os.remove(path)

def safe_rmfile(path):
    if exists(path):
        os.remove(path)

#-------------------------------------------------------------------------------
# dirs
#-------------------------------------------------------------------------------

def mkdir(path):
    os.mkdir(path)
    return path

def safe_mkdir(path):
    if not exists(path):
        mkdir(path)
    return path

def safe_mktree(path):
    '''Creates not only last folder in path but all
    for mktree('1/2/3')
    will create 1/
                1/2
                1/2/3
    '''
    folders = split_path(path)
    for i, folder in enumerate(folders):
        f = os.sep.join(folders[:i+1])
        safe_mkdir(f)
    return path


def rmdir(path):
    """Forced directory remove"""
    def onerror(func, path, exc_info):
        if not os.access(path, os.W_OK):
            os.chmod(path, stat.S_IWUSR)
            func(path)
        else:
            raise

    shutil.rmtree(path, onerror=onerror)

def safe_rmdir(path):
    if exist(path):
        rmtree()


#-------------------------------------------------------------------------------
# upper level
#-------------------------------------------------------------------------------

def remove(path):
    if not exists(path):
        raise Error('object "{}" not found'.format(path))
    if isfile(path):
        rmfile(path)
    elif isdir(path):
        rmdir(path)

    raise Error('unknown object type "{}"'.format(path))


def safe_remove(path):
    if not exists(path):
        return
    remove(path)


def create_structure(structure, path=''):
    '''Creates folder structure in path according dict from parameters
    example:

    structure = {
        folder_l0_1: {                          #this is a folder because dict inside
            folder_l1_1 : {},                   #this is a empty folder inside upper folder
            file_l1_1.txt: 'Hello world!',      #this is file with contents 'Hello world'
            file_l1_2.ext: open('filename.txt') #this will create a file with contents from file stream
        },
        file_l0_1: some text inside # file on top
    }

    create_structure(structure)
    '''
    assert isinstance(structure, dict)
    with work_dir(path):
        for name, data in structure.items():
            assert data is not None
            if isinstance(data, dict):  # create a folder
                safe_mkdir(name)
                create_structure(data, path)
            elif isinstance(data, str): # just a file
                file_write(name, data)
            else:                       # everything else threated as stream
                file_write(name, data.read(), mode='b' if 'b' in data.mode else '')

#-------------------------------------------------------------------------------
# workdirs
#-------------------------------------------------------------------------------

class work_dir(object):
    """change working dir within 'with' context
    Usage:
        with work_dir('otherdir/foo/'):
            print(os.getcwd())
        print(os.getcwd()) # oldone
    """

    def __init__(self, directory):
        self._previous = None
        self._wanted = os.path.abspath(directory)

    def __enter__(self):
        self._previous = os.getcwd()
        os.chdir(self._wanted)
        return self

    def __exit__(self, *args):
        os.chdir(self._previous)
        self._previous = None

    @property
    def current(self):
        return os.getcwd()

    @property
    def previous(self):
        return self._previous

    def __repr__(self):
        return self.current


class work_mkdir(work_dir):
    def __init__(self, path):
        super().__init__(mkdir(path))

class work_safe_mkdir(work_dir):
    def __init__(self, path):
        super().__init__(safe_mkdir(path))


class work_tempdir(work_dir):
    def __init__(self):
        super().__init__(tempfile.mkdtemp())

    def __exit__(self, *args):
        tmp = self.current
        super().__exit__()
        rmdir(tmp)


import unittest
class TestCase(unittest.TestCase):

    def test_1(self):

        import yaml

        with work_tempdir():
            with work_mkdir('.jacis'):
                with work_mkdir('available'):
                    touch('list.yml')
                with work_mkdir('installed'):
                    touch('list.yml')
                with open('config.yml', 'w') as f:
                    import json
                    f.write(json.dumps([1,2,3,4]))

        with work_tempdir():
            struct = {
                ".jacis" : {
                    "available": {
                        "list.yml": ""
                    },
                    "installed": {
                        "list.yml": ""
                    },
                    "config.yml": json.dumps([1,2,3,4])
                }
            }
            create_structure(struct)


        with work_tempdir():
            yml = '''
            .jacis:
                available:
                    list.yml: ""
                installed:
                    list.yml: ""
                config.yml: "[1,2,3,4]"
            '''
            create_structure(yaml.load(yml))



        print(os.getcwd())

        print('-'*100)


        with work_tempdir():
            print('path1: ', os.getcwd())

        with work_tempdir():
            print('path2: ', os.getcwd())


        with work_dir('/usr') as w:
            print(os.getcwd())
            print(w.current)
            print(w.previous)

        print('-'*100)

        print(os.getcwd())
        print(w.current)
