from functools import wraps, partial
from os import path
from nosh import state

def require_args_satisfying_condition(condition, failure):
    """Decorator builder for decorators that should check the given
    condition, and raise the given failure exception if necessary.
    """
    def decorator_maker(arg_indices=None, affect_kwargs=False):
        def decorator(func):
            @wraps(func)
            def new_func(*fargs, **fkwargs):
                affected_indices = arg_indices
                if affected_indices is None:  # apply to all args
                    affected_indices = range(len(fargs))
                for index, arg in enumerate(fargs):
                    if (((index in affected_indices) or
                         ((index - len(fargs)) in affected_indices))
                        and not condition(arg)):
                        raise failure()
                        break
                else:  # all args readable
                    return func(*fargs, **fkwargs)
            return new_func
        return decorator

    return decorator_maker

require_readable_args = require_args_satisfying_condition(state.is_readable,
                                                          state.NotReadableError)

require_writable_args = require_args_satisfying_condition(state.is_writable,
                                                          state.NotWritableError)

def require_arg_state(readable=None, writable=None,
                      kwargs_readable=None, kwargs_writable=None):
    def decorator(func):
        @wraps(func)
        def new_func(*fargs, **fkwargs):
            # check for readable args
            affected_indices = readable
            if affected_indices is None:  # apply to all args
                affected_indices = range(len(fargs))
            for index, arg in enumerate(fargs):
                if (((index in affected_indices) or
                        ((index - len(fargs)) in affected_indices))
                    and not state.is_readable(arg)):
                    raise state.NotReadableError()

            # check for writable args
            affected_indices = writable
            if affected_indices is None:  # apply to all args
                affected_indices = range(len(fargs))
            for index, arg in enumerate(fargs):
                if (((index in affected_indices) or
                        ((index - len(fargs)) in affected_indices))
                    and not state.is_writable(arg)):
                    raise state.NotWritableError()

            return func(*fargs, **fkwargs)
        return new_func
    return decorator

def require_readable_args(*indices, **kwargs):
    return require_arg_state(readable=indices)

def require_writable_args(*indices, **kwargs):
    return require_arg_state(writable=indices)
