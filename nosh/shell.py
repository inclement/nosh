'''
Implementations of file management shell commands.
'''

import os
from os import path
import shutil
import glob
from collections import defaultdict

from nosh.utils import (expand_path, require_args, expand_paths,
                        maybe_exception)
from nosh.wrapperutils import (
    require_readable_args, require_writable_args, require_arg_state)
# from nosh.wrappers import os
# from nosh.wrappers.os import path
# from nosh.wrappers import shutil


@require_args(min=2, max=None)
@expand_paths()
def mv(*args, ignore_errors=False):
    '''Move files from one location to another.

    If the the final argument is a directory, all preceding arguments
    are moved into this dir.

    If the final argument is a filepath, there can only be one other
    argument, which is moved to the target location.

    '''
    target = args[-1]
    sources = args[:-1]

    if not path.isdir(target) and len(sources) > 1:
        maybe_exception(NotADirectoryError,
                        ('Target {} is not a directory but multiple sources '
                         'were specified'.format(target)),
                        ignore_errors)

    if path.isdir(target):
        for source in sources:
            shutil.move(source, target)
    else:
        shutil.move(sources[0], target)


@require_args(min=1)
@expand_paths()
def rm(*args, recursive=False, ignore_errors=False):
    '''
    Delete files and/or directories.

    Parameters
    ----------
    *args : strings
        The file and directory paths to delete. Glob patterns are expanded.
    recursive : bool
        If True, will recursively delete folders and their contents.
        Defaults to False.
    ignore_errors : bool
        If True, will ignore errors when e.g. specified  files do not exist.
        Defaults to False.
    '''
    for arg in args:
        if not path.exists(arg) and ignore_errors:
            continue
        if path.isdir(arg):
            if not recursive:
                error = 'Cannot remove "{}": Is a directory'.format(arg)
                maybe_exception(IsADirectoryError, error, ignore_errors)
            else:
                shutil.rmtree(arg, ignore_errors=ignore_errors)
        else:
            os.unlink(arg)


@require_args(min=2)
@expand_paths()
@require_readable_args()
@require_writable_args(-1)
def cp(*args, recursive=False, ignore_errors=False):
    '''Copy files and/or directories.

    Parameters
    ----------
    *args : strings
        The names of files to copy, and target directory. The final arg is the
        target filepath/directory, all preceding args are copied. Each path
        is expanded as a glob pattern.
    recursive : bool
        Whether to copy directories (recursively). 
    '''
    target = args[-1]
    sources = args[:-1]

    print('isdir is', path.isdir)

    if not path.isdir(target) and len(sources) > 1:
        maybe_exception(NotADirectoryError,
                        ('Target is not a directory but multiple '
                         'sources were specified'),
                        ignore_errors)

    if path.isdir(target):
        for source in sources:
            if path.isdir(source):
                if recursive:
                    dir_name = path.basename(source)
                    shutil.copytree(source, path.join(target, dir_name))
                else:
                    maybe_exception(IsADirectoryError,
                                    ('Tried to copy directory but '
                                     'recursive is False.'),
                                    ignore_errors)
            else:
                shutil.copy(source, target)
    else:
        source = sources[0]

        if path.isdir(source) and path.exists(target):
            maybe_exception(NotADirectoryError,
                            ('Cannot copy directory to file that '
                             'already exists'),
                            ignore_errors)
        elif path.isdir(source):
            if recursive:
                shutil.copytree(source, target)
            else:
                maybe_exception(IsADirectoryError,
                                ('Tried to copy directory but '
                                 'recursive is False.'),
                                ignore_errors)
        else:
            shutil.copy(source, target)


def pwd():
    return expand_path(os.curdir)


@expand_paths(do_glob=False)
def ls(*args):
    if not args:
        args = ['.']
    results = defaultdict(lambda: [])
    for arg in args:
        if path.isdir(arg):
            results[arg] = os.listdir(arg)
        elif path.exists(arg):  # arg is a file
            results[path.dirname(arg)].append(arg)
        else:
            results[path.dirname(arg)].extend(glob.glob(arg))
    if len(results) == 1:
        return results[list(results.keys())[0]]
    return results


@expand_paths(do_glob=False)
def mkdir(dir_name, mode=511, parents=False, exist_ok=False):
    if path.exists(dir_name):
        if not exist_ok:
            raise FileExistsError(
                'Cannot make dir at {}, it already exists'.format(dir_name))
        else:
            return
    if parents:
        os.makedirs(dir_name, mode=mode, exist_ok=exist_ok)
    else:
        os.mkdir(dir_name, mode=mode)


@expand_paths()
def touch(*args):
    '''Highly incomplete touch implementation (currently only can create
    empty files or touch existing ones).
    '''
    for filen in args:
        if path.isdir(filen):
            raise OSError(
                'Cannot touch {}, directory of that name exists'.format(filen))
        if not path.exists(filen):
            with open(filen, 'w'):
                pass
        else:
            with open(filen, 'r'):
                pass
