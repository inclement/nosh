
import nosh as no
import nosh.utils as noutils
import nosh.dirutils as nodirutils

from os import path
import os

import pytest

DIR_NAMES = ('dir1', )
FILE_NAMES = ['{}.txt'.format(i) for i in range(5)]

def create_example_files():
    for dir_name in DIR_NAMES:
        os.mkdir(dir_name)
    for file_name in FILE_NAMES:
        with open(file_name, 'w') as fileh:
            pass

    with open('text_file.txt', 'w') as fileh:
        fileh.write('text in file')

    no.touch(path.join('dir1', 'dir_file.txt'))

def temp_dir(func):
    '''Decorator to carry out tests in a py.test temp dir.'''
    def new_func(*args, **kwargs):
        with nodirutils.temp_directory() as temp_dir_name:
            with nodirutils.current_directory(temp_dir_name):
                create_example_files()
                return func(*args, **kwargs)
    return new_func


class TestTar(object):
    @temp_dir
    def test_tar_too_few_args(self):
        with pytest.raises(ValueError):
            no.tar()
        with pytest.raises(ValueError):
            no.tar('1.txt')

    @temp_dir
    def test_target_exists(self):
        with pytest.raises(FileExistsError):
            no.tar('*.txt', 'text_file.txt')

    @temp_dir
    def test_target_does_not_exist(self):
        with pytest.raises(FileNotFoundError):
            no.tar('*.txt', 'tar_archive_not_present.tar.gz', append=True)

    @temp_dir
    def test_target_exists(self):
        no.touch('existing.tar.gz')
        with pytest.raises(FileExistsError):
            no.tar('*.txt', 'existing.tar.gz')

    @temp_dir
    def test_tar(self):
        no.tar('*.txt', 'tarfile.tar.gz')

        import tarfile
        with tarfile.open('tarfile.tar.gz', 'r') as tarh:
            members = tarh.getmembers()
        paths = [m.path for m in members]
        for file_name in FILE_NAMES:
            assert file_name in paths
            
