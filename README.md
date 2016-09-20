
# nosh

Nosh provides pure Python functions for file manipulation (moving,
copying, deleting etc.) and other shell-like tasks such as directory
listing and archive management.

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
