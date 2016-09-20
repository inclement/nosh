from setuptools import setup, find_packages

packages = find_packages()

setup(
    name='nosh',
    version='0.1',
    description='Shell-like tools in pure Python',
    author='Alexander Taylor',
    author_email='alexanderjohntaylor@gmail.com',
    packages=packages,
    package_data={'nosh': ['*.py']}
)
