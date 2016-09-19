
import shutil
import os
from os import path
from functools import wraps
import contextlib

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
        for arg in args:
            shutil.move(arg, target)
    else:
        shutil.move(sources[0], target)
            

@_require_args(min=1)
@_expand_paths
def rm(*args, recursive=False, dir=False, ignore_errors=False):
    for arg in args:
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

def cp(*args, recursive=False):
    pass

def pwd():
    return expand_path(os.curdir)


def ls(path='.'):
    return os.listdir(path)

def mkdir(dir_name, mode=511, parents=False, exist_ok=False):
    if parents:
        os.makedirs(dir_name, mode=mode, exist_ok=exist_ok)
    else:
        if path.exists(dir_name):
            if exist_ok:
                return
        os.mkdir(dir_name, mode=mode)

def ln(source, target, softlink=False):
    pass

def expand_path(input):
    return path.abspath(path.expanduser(input))

@contextlib.contextmanager
def current_directory(new_dir):
    '''Context manager to temporarily move to a different directory.

    '''
    new_dir = expand_path(new_dir)
    cur_dir = os.getcwd()
    print('-> context {}'.format(new_dir))
    os.chdir(new_dir)
    yield
    print('<- context {}'.format(cur_dir))
    os.chdir(cur_dir)
