import nosh.shell as no
import nosh.utils as noutils

from os import path
import os

import inspect

import pytest

DIR_NAMES = ('dir1', 'dir2')
FILE_NAMES = ['{}.txt'.format(i) for i in range(5)]


def temp_dir(func):
    '''Decorator to carry out tests in a py.test temp dir.'''
    num_params = len(inspect.signature(func).parameters)
    if num_params == 0:
        def test_funcname(tmpdir):
            tmpdir = path.join(tmpdir.dirname, tmpdir.basename)
            with noutils.current_directory(tmpdir):
                result = func()
            return result
    elif num_params == 1:
        def test_funcname(self, tmpdir):
            tmpdir = path.join(tmpdir.dirname, tmpdir.basename)
            with noutils.current_directory(tmpdir):
                result = func(self)
            return result
    else:
        raise ValueError('Decorator can only be applied to functions '
                         'with 0 or 1 argument')
    return test_funcname

def create_example_files():
    for dir_name in DIR_NAMES:
        os.mkdir(dir_name)
    for file_name in FILE_NAMES:
        with open(file_name, 'w') as fileh:
            pass

    with open('text_file.txt', 'w') as fileh:
        fileh.write('text in file')

@temp_dir
def test_create_example_files():
    create_example_files()
    for dir_name in DIR_NAMES:
        assert path.exists(dir_name)
        assert path.isdir(dir_name)
    for file_name in FILE_NAMES:
        assert path.exists(file_name)
        assert path.isfile(file_name)
            

@temp_dir
def test_mkdir():
    no.mkdir('test_dir')
    assert path.exists('test_dir')
    assert path.isdir('test_dir')


@temp_dir
def test_touch():
    assert not path.exists('test.txt')
    no.touch('test.txt')
    assert path.exists('test.txt')
    assert path.isfile('test.txt')
    

class TestCp(object):
    @temp_dir
    def test_cp_one_file(self):
        create_example_files()

        assert not path.exists('cp_file.txt')
        no.cp('text_file.txt', 'cp_file.txt')
        assert path.exists('cp_file.txt') and path.isfile('cp_file.txt')

        with open('cp_file.txt', 'r') as fileh:
            assert fileh.read() == 'text in file'

    @temp_dir
    def cp_to_dir(self):
        create_example_files()
        assert path.exists('dir1')
        assert path.isdir('dir1')
        assert not os.listdir('dir1')
        no.cp('*.txt', 'dir1')
        for file_name in FILE_NAMES:
            assert(path.exists(path.join('dir1', file_name)))

        with open(path.join('dir1', 'text_file.txt'), 'r') as fileh:
            assert fileh.read() == 'text in file'

    @temp_dir
    def test_cp_dir_fail(self):
        create_example_files()

        assert path.exists('dir1')
        assert not path.exists('newdir')
        no.cp('dir1', 'newdir')
        assert not path.exists('newdir')

    @temp_dir
    def test_cp_dir_success(self):
        create_example_files()

        assert path.exists('dir1')
        assert not path.exists('newdir')
        no.cp('dir1', 'newdir', recursive=True)
        assert path.exists('newdir')

    @temp_dir
    def test_cp_dir_recursive(self):
        create_example_files()

        with open(path.join('dir2', 'file.txt'), 'w') as fileh:
            fileh.write('file contents')
        assert path.exists('dir1')
        assert not path.exists('newdir')
        no.cp('dir2', 'newdir', recursive=True)
        assert path.exists('newdir')

        with open(path.join('newdir', 'file.txt'), 'r') as fileh:
            assert fileh.read() == 'file contents'
