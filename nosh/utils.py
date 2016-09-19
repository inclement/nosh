'''
Utilities for other functions.
'''

import contextlib
import os
from os import path
import shutil
from functools import wraps
import glob

@contextlib.contextmanager
def current_directory(new_dir):
    '''Context manager to temporarily move to a different directory.

    '''
    new_dir = expand_path(new_dir)
    cur_dir = os.getcwd()
    os.chdir(new_dir)
    yield
    os.chdir(cur_dir)

def expand_path(input):
    return path.abspath(path.expanduser(input))

def _get_num_args_text(min, max):
    if min is not None and max is not None:
        return '{} to {} arguments'.format(min, max)
    elif min is not None:
        return 'at least {} argument{}'.format(
            min, 's' if min > 1 else '')
    elif max is not None:
        return 'no more than {} arguments'.format(max)
    else:
        return 'any number of arguments'

def require_args(min=None, max=None,
                  errors={None: 'Invalid number of arguments'}):
    '''Decorator that checks if the function has received a valid number
    of arguments.

    Parameters
    ----------
    min : int or None
        The minimum number of arguments the function must accept.
        Defaults to None (no minimum).
    max : int or None
        The maximum number of arguments the function must accept
        Defaults to None (no maximum).
    '''
    def require_args_decorator(func):
        @wraps(func)
        def new_func(*args, **kwargs):
            if max is not None and len(args) > max:
                raise TypeError('{} takes {}, but {} given'.format(
                    func, _get_num_args_text(min, max), len(args)))
            elif min is not None and len(args) < min:
                raise TypeError('{} takes {}, but {} given'.format(
                    func, _get_num_args_text(min, max), len(args)))
            return func(*args, **kwargs)
        return new_func
    return require_args_decorator

def expand_paths(*args, do_glob=True):
    '''Assumes all the args of func are paths, and expands them.

    If any args are passed, the function's kwargs are also expanded as
    paths if they match one of the args.

    Parameters
    ----------
    do_glob : bool
        If True, glob patterns in the args are expanded. Defaults to True. 
    '''
    def expand_paths_decorator(func):
        @wraps(func)
        def new_func(*fargs, **fkwargs):
            fargs = [expand_path(arg) for arg in fargs]
            if do_glob:
                new_args = []
                for arg in fargs:
                    if not glob_pattern_present(arg):
                        new_args.append(arg)
                    else:
                        new_args.extend(glob.glob(arg))
                fargs = new_args
            
            for kwarg in fkwargs:
                if kwarg in args:
                    fkwargs[kwarg] = expand_path(fkwargs[kwarg])
                
            return func(*fargs, **fkwargs)
        return new_func
    return expand_paths_decorator

def glob_pattern_present(string):
    return any([c in string for c in ('*?[]')])
