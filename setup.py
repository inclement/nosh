
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='nosh',
    version='0.1',
    description='Shell-like tools in pure Python',
    author='Alexander Taylor',
    author_email='alexanderjohntaylor@gmail.com',
    packages=['nosh'],
    url='https://github.com/inclement/nosh',
)
