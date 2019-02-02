import nosh as no
from nosh import state
from functools import wraps

DEFAULT_READABLE_PATHS = {'/'}
DEFAULT_WRITABLE_PATHS = {'/'}

EXAMPLE_PATHS = ['/foo/bar', '/moo/cow']

def assert_default_readable_writable():
    assert state.get_readable() == DEFAULT_READABLE_PATHS
    assert state.get_writable() == DEFAULT_WRITABLE_PATHS

def check_begin_end_default(func):
    """Check that the readable and writable directories match the
    expected defaults both before and after the test has run.
    """
    @wraps(func)
    def new_func(*args, **kwargs):
        assert_default_readable_writable()
        func(*args, **kwargs)
        assert_default_readable_writable()
    return new_func

@check_begin_end_default
def test_push_readable():
    with state.push_readable('test'):
        assert state.get_readable() == DEFAULT_READABLE_PATHS.union({'test'})

@check_begin_end_default
def test_push_writable():
    with state.push_writable('test'):
        assert state.get_writable() == DEFAULT_WRITABLE_PATHS.union({'test'})

@check_begin_end_default
def test_push_valid():
    with state.push_valid('name'):
        assert state.get_readable() == DEFAULT_READABLE_PATHS.union({'name'})
        assert state.get_writable() == DEFAULT_WRITABLE_PATHS.union({'name'})

@check_begin_end_default
def test_set_readable():
    with state.set_readable(*EXAMPLE_PATHS):
        assert state.get_readable() == set(EXAMPLE_PATHS)

@check_begin_end_default
def test_set_writable():
    with state.set_writable(*EXAMPLE_PATHS):
        assert state.get_writable() == set(EXAMPLE_PATHS)

@check_begin_end_default
def test_set_valid():
    with state.set_valid(*EXAMPLE_PATHS):
        assert state.get_readable() == set(EXAMPLE_PATHS)
        assert state.get_writable() == set(EXAMPLE_PATHS)

@check_begin_end_default
def test_no_valid_paths():
    with state.no_valid_paths():
        assert state.get_readable() == set()
        assert state.get_writable() == set()

def test_is_subpath():
    # Test some example constructed paths
    assert state.is_subpath('/', ['/'])
    assert state.is_subpath('/foo/bar', ['/foo'])
    assert state.is_subpath('/foo/bar', ['/foo/bar', '/bar'])
    assert state.is_subpath('/foo/bar/cow', ['/foo/bar'])
    assert state.is_subpath('/foo/bar/cow', ['/foo/bar', '/foo'])
    assert state.is_subpath('/foo/bar/cow', ['/foo/bar', '/foo', '/foo/bar/cow'])
    assert not state.is_subpath('/', [])
    assert not state.is_subpath('/', ['/foo'])
    assert not state.is_subpath('/foo/bar', ['/foo/bar/cow'])
    assert not state.is_subpath('/foo/bar', ['/foo/bare'])
    assert not state.is_subpath('/foo/bar', ['/foo/ba'])

def test_is_readable():
    assert state.is_readable('/foo/bar/file.txt')
    with state.set_readable():
        assert not state.is_readable('/foo/bar/file.txt')
    with state.set_readable('/foo/bar'):
        assert state.is_readable('/foo/bar/file.txt')
    assert state.is_readable('/foo/bar/file.txt')

def test_is_writable():
    assert state.is_writable('/foo/bar/file.txt')
    with state.set_writable():
        assert not state.is_writable('/foo/bar/file.txt')
    with state.set_writable('/foo/bar'):
        assert state.is_writable('/foo/bar/file.txt')
    assert state.is_writable('/foo/bar/file.txt')
