'''Module for maintaining and manipulating nosh's global state
regarding directories that are currently readable or writable.  '''

from contextlib import contextmanager
from os.path import isdir, isfile, relpath, split
from collections import defaultdict
import copy

READABLE_PATHS_STACK = []
WRITABLE_PATHS_STACK = []
CURRENT_READABLE_PATHS = set('/')
CURRENT_WRITABLE_PATHS = set('/')
RESTRICT_PATHS = False

def _push_readable():
    READABLE_PATHS_STACK.append(CURRENT_READABLE_PATHS.copy())

def _push_writable():
    WRITABLE_PATHS_STACK.append(CURRENT_WRITABLE_PATHS.copy())

def _pop_readable():
    global CURRENT_READABLE_PATHS
    CURRENT_READABLE_PATHS = READABLE_PATHS_STACK.pop()

def _pop_writable():
    global CURRENT_WRITABLE_PATHS
    CURRENT_WRITABLE_PATHS = WRITABLE_PATHS_STACK.pop()

def get_readable():
    return CURRENT_READABLE_PATHS

def get_writable():
    return CURRENT_WRITABLE_PATHS

@contextmanager
def push_readable(*args):
    global CURRENT_READABLE_PATHS
    _push_readable()
    for arg in args:
        CURRENT_READABLE_PATHS.add(arg)
    yield
    _pop_readable()
            
@contextmanager
def push_writable(*args):
    global CURRENT_WRITABLE_PATHS
    _push_writable()
    for arg in args:
        CURRENT_WRITABLE_PATHS.add(arg)
    yield
    _pop_writable()

@contextmanager
def push_valid(*args):
    with push_readable(*args), push_writable(*args):
        yield

@contextmanager
def set_readable(*args):
    global CURRENT_READABLE_PATHS
    _push_readable()
    CURRENT_READABLE_PATHS = set(args)
    yield
    _pop_readable()
    
@contextmanager
def set_writable(*args):
    global CURRENT_WRITABLE_PATHS
    _push_writable()
    CURRENT_WRITABLE_PATHS = set(args)
    yield
    _pop_writable()

@contextmanager
def set_valid(*args):
    with set_readable(*args), set_writable(*args):
        yield

@contextmanager
def no_valid_paths():
    """
    Context manager that clears the list of readable and writable paths.
    """
    with set_valid():
        yield

def is_readable(path):
    return is_subpath(path, CURRENT_READABLE_PATHS)

def is_writable(path):
    return is_subpath(path, CURRENT_WRITABLE_PATHS)

def is_subpath(path, start_paths):
    for start_path in start_paths:
        relative_path = relpath(path, start=start_path)
        dir_step = ''

        # keep splitting the path until we hit the first element
        while relative_path != '':
            relative_path, dir_step = split(relative_path)

        # relpath will return ../something if the path is not a
        # subpath of the start path
        if not dir_step == '..':
            return True
    return False
    

class NotReadableError(Exception):
    pass
