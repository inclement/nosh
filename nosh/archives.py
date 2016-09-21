'''Implementations of commands dealing with archives (tar, zip etc.).

These do *not* correspond directly to the shell commands, e.g. instead
of using tar for both creating and unpacking tarballs nosh provides
``tar`` for compressing and ``untar`` for extracting.

'''

import os
from os import path
from nosh.utils import (expand_path, require_args, expand_paths,
                        maybe_exception)
import shutil

import tarfile
import zipfile


@require_args(min=2)
@expand_paths()
def tar(*args, compress='gzip', append=False):
    '''Create or append to tarballs.

    Parameters
    ----------
    *args : strings
        The files and directories to place in the tarball. The final argument should be
        the tarball name.
    compress : str or False
        Whether to compress the tarball. May be 'gzip', 'bz2' or False.
        Defaults to 'gzip'.
    append : bool
        Whether to append to the tarball. Will raise an exception if the
        path does not exist. Defaults to False.

    TODO
    ----
    compress should be more flexible, to work with tarballs with different
    compression types.
    '''
    pass

@expand_paths('target', do_glob=False)
def untar(tar_path, target='.', compress='auto'):
    '''Extract the given tarball.

    Parameters
    ----------
    tar_path : str
        The path to tarball to be extracted.
    target : str
        The directory to extract to. Defaults to '.', the current dir.
    compress : str
        Whether the tarfile is compressed. Defaults to auto, which will
        automatically work with gzip or bz2. You can also specify these
        explicitly, but probably don't want to. Other compression formats
        are not supported.
    '''
    pass
    

@expand_paths()
def lstar(tar_path, compress='auto'):
    '''Get the contents of the given tarball.

    Parameters
    ----------
    tar_path : str
        The path to the tarfile.
    compress : str
        Whether the tarfile is compressed. Defaults to auto, which will
        automatically work with gzip or bz2. You can also specify these
        explicitly, but probably don't want to. Other compression formats
        are not supported.
    '''
    pass
