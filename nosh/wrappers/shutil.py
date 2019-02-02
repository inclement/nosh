import shutil
from nosh.wrapperutils import require_readable_args, require_writable_args


copy = require_readable_args()(require_writable_args(arg_indices=[-1])(shutil.copy))
