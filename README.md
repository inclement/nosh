
# nosh

Nosh is a pure Python API to the commands you might normally perform
in the shell, such as moving, copying or deleting files, listing
directories, extracting or exploring archives etc.

Nosh implements Python functions inspired by common shell commands
such as mv, ls, cp etc. It does not try to strictly copy their
functionality, but to follow their semantics, and to expose a much
clearer API than Python's builtin libraries.

Since nosh uses only Python's own builtin functions internally, it
should work on any platform supported by Python (as opposed to shell
calling solutions such as the sh module).

## Philosophy

I created nosh after becoming frustrated with the file management
functions of Python's standard library, spread across `os`, `os.path`,
`shutil` and other modules. This API seems very inconsistent and
inconvenient, with poorly labelled similar functions - for instance,
the actions you'd accomplish with the `cp` shell command are spread
across `shutil.copy`, `shutil.copy2`, `shutil.copyfile`,
`shutil.copytree` and several others! These do not all have the same
semantics, e.g. `shutil.copy` can copy a file inside a destination
folder, while `shutil.copytree` copies to the strict destination name,
which cannot already exist.

nosh's functions are inspired by the shell equivalents, but are simple
alternatives that do not try to fully implement them. For
instance, instead of having to check if a file is a directory
etc. before deciding what copy function to use, you can use code like:

    nosh.cp('*.txt', 'example.mp3', 'some_folder_name', 'destination')

This copies all those files and folders to inside the destination
folder, it is equivalent to `mv *.txt example.mp3 some_folder_name
destination`.

