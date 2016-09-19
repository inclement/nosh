
import shutil
import os
from os import path
from functools import wraps

def _get_num_args_text(min, max):
    if min is not None and max is not None:
        '{} to {} arguments'.format(min, max)
    elif min is not None:
        'at least {} arguments'.format(min)
    elif max is not None:
        'no more than {} arguments'.format(max)
    else:
        'any number of arguments'

def _require_args(min=None, max=None,
                  errors={None: 'Invalid number of arguments'}):
    '''Decorator that checks if the function has received a valid number
    of arguments.'''
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

def _expand_paths(func):
    '''Assumes all the args of func are paths, and expands them.'''
    @wraps(func)
    def new_func(*args, **kwargs):
        args = [expand_path(arg) for arg in args]
        return func(*args, **kwargs)
    return new_func

@_require_args(min=2, max=None)
def mv(*args):
    target = args[-1]
    sources = args[:-1]
    
    if not path.isdir(target) and len(sources) > 1:
        raise ValueError('Target is not a directory but multiple '
                         'sources were specified')

    if path.isdir(target):
        pass

    else:
        pass

@_expand_paths
def rm(*args, recursive=False, dir=False, ignore_errors=False):
    for arg in args:
        print('would delete {}, is dir {}'.format(arg, path.isdir(arg)))
        if not path.exists(arg) and ignore_errors:
            continue
        if path.isdir(arg):
            if not recursive:
                error = 'Cannot remove "{}": Is a directory'.format(arg)
                if ignore_errors:
                    print(error)
                else:
                    raise OSError(error)
            else:
                shutil.rmtree(arg, ignore_errors=ignore_errors)
        else:
            os.unlink(arg)

def pwd():
    return expand_path(os.curdir)

def cp(*args, recursive=False):
    pass

def ls(path='.'):
    pass

def mkdir(path, parents=False):
    pass

def ln(source, target, softlink=False):
    pass

def expand_path(input):
    return path.abspath(path.expanduser(input))

def current_directory(path):
    pass
