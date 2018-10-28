'''Implementations of commands dealing with archives (tar, zip etc.).

These do *not* correspond directly to the shell commands, e.g. instead
of using tar for both creating and unpacking tarballs nosh provides
``tar`` for compressing and ``untar`` for extracting.

'''

from os import path
from nosh.utils import (require_args, expand_paths,
                        maybe_exception)

import tarfile
import zipfile


@require_args(min=2)
@expand_paths(abspath=False)
def tar(*args, compress='gz', append=False):
    '''Create or append to tarballs.

    Parameters
    ----------
    *args : strings
        The files and directories to place in the tarball. The final argument
        should be the tarball name.
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
    sources = args[:-1]
    target = args[-1]

    if compress not in [None, 'gz', 'bz2']:
        raise ValueError(
            'compress must be one of {}'.format([None, 'gz', 'bz2']))

    if not append and path.exists(target):
            raise FileExistsError(
                ('Cannot create tar at target {}, file already '
                 'exists').format(target))

    if append and not path.exists(target):
        raise FileNotFoundError(
            'Cannot append to archive {}, it does not exist'.format(target))

    if append:
        if compress is not None:
            raise ValueError(
                ('Appending to compressed ({}) tarfiles not '
                 'supported').format(compress))
        tarh = tarfile.open(target, mode='a')
    else:
        if compress is None:
            compress = '*'
        tarh = tarfile.open(target, mode='w:{}'.format(compress))

    with tarh:
        for source in sources:
            tarh.add(source)


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

    TODO
    ----
    include and exclude arguments
    '''

    if not path.exists(tar_path):
        raise FileNotFoundError('Tarfile {} does not exist'.format(tar_path))

    if not path.exists(target) or not path.isdir(target):
        raise FileNotFoundError(
            'Cannot extract to {}, path does not exist'.format(target))

    if compress in (None, 'auto'):
        compress = '*'

    with tarfile.open(tar_path, 'r:{}'.format(compress)) as tarh:
        tarh.extractall(target)


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
    if compress not in ('auto', 'gz', 'bz2'):
        raise ValueError(
            'compress must be one of {}'.format('auto', 'gz', 'bz2'))

    if not path.exists(tar_path):
        raise FileNotFoundError(
            'tarfile at {} does not exist'.format(tar_path))

    if compress == 'auto':
        compress = '*'

    with tarfile.open(tar_path, mode='r:{}'.format(compress)) as tarh:
        members = tarh.getmembers()

    return members


@require_args(min=2)
@expand_paths(abspath=False)
def zip(*args):
    sources = args[:-1]
    target = args[-1]

    if path.exists(target):
        raise FileExistsError('Cannot zip to {}, file exists'.format(target))

    with zipfile.ZipFile(target, 'w') as ziph:
        for source in sources:
            ziph.write(source)
        
