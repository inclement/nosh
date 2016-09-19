
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

def _require_args(func, min=None, max=None,
                  errors={_: 'Invalid number of arguments'}):
    '''Decorator that checks if the function has received a valid number
    of arguments.'''
    @wraps(func)
    def new_func(*args, **kwargs):
        if max is not None and len(args) > max:
            raise TypeError('{} takes {}, but {} given'.format(
                func, _get_num_args_text(min, max), len(args)))
        elif min is not None and len(args) < min:
            raise TypeError('{} takes {}, but {} given'.format(
                func, _get_num_args_text(min, max), len(args)))
        return func(*args, **kwargs)

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

def rm(*args, recursive=False, dir=False):
    pass

def pwd():
    pass

def cp(*args, recursive=False):
    pass

def ls(path='.'):
    pass

def mkdir(path, parents=False):
    pass

def ln(source, target, softlink=False):
    pass



def expand_path(path):
    # Apply all of realpath, expanduser etc.
    pass

def current_directory(path):
    pass
