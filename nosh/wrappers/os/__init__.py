"""Wrappers around Python's os module and submodule functions,
calling the original functions only if their arguments are currently
allowed by nosh's global state.  """

from nosh.wrapperutils import require_writable_args
import os

curdir = os.curdir

makedirs = require_writable_args(os.makedirs)
