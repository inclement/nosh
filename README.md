
# nosh

Nosh stands for **no** **sh**ell. It provides pure Python functions
for file manipulation (moving, copying, deleting etc.) and other
shell-like tasks such as directory listing and archive management,
with a consistent API.

Nosh implements Python functions inspired by common shell commands
such as mv, ls, cp etc. It does not try to strictly copy their
functionality and arguments, but to follow their semantics, and to
expose a clearer API than Python's builtin libraries. Nosh also
provides extra helper functions, such as a context manager for
switching directories within a block.

Since nosh uses only Python's own builtin functions internally, it
should work on any platform supported by Python (as opposed to tools
like the sh module that directly call the real commands).

## Philosophy

I created nosh after becoming frustrated with the file management
functions of Python's standard library, spread across `os`, `os.path`,
`shutil` and other modules. This API is inconsistent and
inconvenient - for instance, the actions you'd accomplish with the
`cp` shell command are spread across `shutil.copy`, `shutil.copy2`,
`shutil.copyfile`, `shutil.copytree` and several others! These do not
all have the same semantics, e.g. `shutil.copy` can copy a file to
inside a target folder, while `shutil.copytree` requires that the
target folder does not already exist. There may be good reasons for
these distinctions, but it doesn't make for simple code.

nosh's functions are inspired by the shell equivalents, but are simple
alternatives that do not try to fully implement them. For
instance, instead of having to check if a file is a directory
etc. before deciding what copy function to use, you can use code like
the following:

```python
# shell command (`target` is a directory)
cp *.txt example.mp3 some_folder_name target

# nosh
import nosh
nosh.cp('*.txt', 'example.mp3', 'some_folder_name', 'target')

# Python stdlib
import glob
import shutil
from os.path import join
filens = glob.glob('*.txt') + ['example.mp3']
for filen in filens:
    shutil.copy(filen, 'target')
shutil.copytree('some_folder_name', join('target', 'some_folder_name'))
```

## Examples

    

## Other features

### Unexpected operations

Unlike the shell, nosh tries to raise errors rather than continuing
processing when e.g. you try to copy a directory without
recursive=True (whereas `cp` would just print `cp: omitting directory
'dirname'`). You can tell individual commands to ignore such problems
by passing `ignore_errors=True`.

### Directory convenience utilities

nosh provides some utilities for working with directories.

Temporarily moving into a directory:

```python
from nosh import current_directory
with current_directory('some_dir_name'):
    # within this block, we are in `some_dir_name`
    print(nosh.pwd())  # will print /path/to/some_dir_name
```

Creating a temporary directory that is removed outside the context:

```python
from nosh import temp_directory
from os.path import exists
with temp_directory() as temp_dir:
    print(temp_dir)  # will print something like /tmp/tmpsg_kdx64
print(exists(temp_dir))  # False
```

