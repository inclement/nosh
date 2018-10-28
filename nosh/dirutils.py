import contextlib
import os
import shutil
import tempfile

from nosh.utils import expand_path

@contextlib.contextmanager
def current_directory(new_dir):
    '''Context manager to temporarily move to a different directory.

    '''
    new_dir = expand_path(new_dir)
    cur_dir = os.getcwd()
    os.chdir(new_dir)
    yield
    os.chdir(cur_dir)

@contextlib.contextmanager
def temp_directory(clean=True):
    '''Context manager returning a temporary directory name.  This
    directory, and all its contents, is deleted at the end of the
    context.

    Parameters
    ----------
    clean : bool
        Whether to delete the temp dir after use. Defaults to True.
        The main reason to set False is for testing purposes.
    '''
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    if clean:
        shutil.rmtree(temp_dir)

