
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

Here are some examples of basic nosh functionality:

```python
import nosh as no

# Create some files and directories
for i in range(5):
no.touch('{}.txt'.format(i))  # no.touch creates the files
no.mkdir('dir1')
no.mkdir('dir2/dir2_contents', parents=True)
    # when parents=True, both dirs are created
    # if parents=False, this would raise an error
no.mkdir('dir3')

print(no.ls())  # ['1.txt', '4.txt', '3.txt', '2.txt', '0.txt', 'dir2', 'dir1']

# Copy files around
no.cp('1.txt', '1_copy.txt')
print(no.ls())  # ['1.txt', '4.txt', '3.txt', '1_copy.txt', '2.txt', '0.txt', 'dir2', 'dir1']

no.cp('[1-3].txt', 'dir1')  # glob patterns are supported
print(no.ls('dir1'))  # ['1.txt', '3.txt', '2.txt']

no.cp('dir2', 'dir1', recursive=True) # Directories can be copied the same way
print(no.ls('dir1'))  # ['1.txt', '3.txt', '2.txt', 'dir2']
print(no.ls('dir1/dir2'))  # ['dir2_contents']

# Move files
print(no.ls())  # ['1.txt', '4.txt', '3.txt', '1_copy.txt', '2.txt', '0.txt', 'dir2', 'dir1']
print(no.ls('dir3'))  # []

no.mv('1.txt', 'dir3')
print(no.ls())  # ['4.txt', '3.txt', '1_copy.txt', '2.txt', 'dir3', '0.txt', 'dir2', 'dir1']
print(no.ls('dir3'))  # ['1.txt']

no.mv('2.txt', 'dir3/moved_2.txt')  # Moving files can rename them
print(no.ls())  # ['4.txt', '3.txt', '1_copy.txt', 'dir3', '0.txt', 'dir2', 'dir1']
print(no.ls('dir3'))  # ['1.txt', 'moved_2.txt']

# Delete files
no.rm('1_copy.txt')
print(no.ls())  # ['4.txt', '3.txt', 'dir3', '0.txt', 'dir2', 'dir1']

no.rm('dir3', recursive=True)  # Can also delete directories
print(no.ls())  # ['4.txt', '3.txt', '0.txt', 'dir2', 'dir1']

no.rm('*.txt')  # Glob patterns can be used here too
                # (and in most other commands)
print(no.ls())  # ['dir2', 'dir1']

no.rm('*', recursive=True)  # Clean all the directories
print(no.ls())  # []
```

## Other features

### Fail on unexpected behaviour

Unlike the shell, nosh tries to raise errors rather than continuing
processing when e.g. you try to copy a directory without
recursive=True (whereas `cp` would just print `cp: omitting directory
'dirname'`). You can tell individual commands to ignore such problems
for more shell-like behaviour by passing `ignore_errors=True`.

```bash
# in bash
mkdir testdir
cp testdir testdir2  # prints 'cp: omitting directory 'testdir''
cp -r testdir testdir2  # works
```

```python
# in Python with nosh
import nosh as no
no.mkdir('testdir')
no.cp('testdir', 'testdir2')  # raises IsADirectoryError
no.cp('testdir', 'testdir2', recursive=True)  # works
no.cp('testdir', 'testdir2', ignore_errors=True) 
    # prints 'Error: Tried to copy directory but recursive is False.'
    # but does not raise an exception and would process other args

```

### Directory convenience utilities

nosh provides some utilities for working with directories.

Temporarily moving into a directory:

```python
from nosh import current_directory, pwd
with current_directory('some_dir_name'):
    # within this block, we are in `some_dir_name`
    print(pwd())  # will print /path/to/some_dir_name
```

Creating a temporary directory that is removed outside the context:

```python
from nosh import temp_directory
from os.path import exists
with temp_directory() as temp_dir:
    print(temp_dir)  # will print something like /tmp/tmpsg_kdx64
print(exists(temp_dir))  # False
```

