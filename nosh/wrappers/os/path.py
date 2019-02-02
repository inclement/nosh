from nosh.wrapperutils import require_readable_args

from os import path

isdir = require_readable_args()(path.isdir)

exists = require_readable_args()(path.exists)

