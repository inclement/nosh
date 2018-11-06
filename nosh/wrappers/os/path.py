from functools import wraps
from nosh import state

from os import path

def require_readable_args(func):
    @wraps(func)
    def new_func(*fargs, **fkwargs):
        for arg in fargs:
            if not state.is_readable(arg):
                raise state.NotReadableError()
                break
        else:  # all args readable
            func(*fargs, **fkwargs)

isdir = require_readable_args(path.isdir)
