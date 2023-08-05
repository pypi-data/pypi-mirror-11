#!/usr/bin/env python

from setuptools import setup
from setuptools.command.test import test as TestCommand
import sys

_PY26 = sys.version_info[:2] == (2,6)

class Tox(TestCommand):
    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]
    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import tox
        import shlex
        args = self.tox_args
        if args:
            args = shlex.split(self.tox_args)
        errno = tox.cmdline(args=args)
        sys.exit(errno)


def linelist(text):
    """
    Returns each non-blank line in text enclosed in a list.
    """
    return [l.strip() for l in text.strip().splitlines() if l.split()]
    
    # The double-mention of l.strip() is yet another fine example of why
    # Python needs en passant aliasing.

if _PY26:
	requires = ['stuf<=0.9.14']
else:
	requires = ['stuf>=0.9.16']

setup(
    name='otherstuf',
    version="1.0.0",
    author='Jonathan Eunice',
    author_email='jonathan.eunice@gmail.com',
    description='Attributes-accessible mappings chainstuf (like ChainMap) & counterstuf (like Counter)',
    long_description=open('README.rst').read(),
    url='https://bitbucket.org/jeunice/otherstuf',
    license='Apache License 2.0',
    packages=['otherstuf'],
    install_requires=requires,
    tests_require=['tox', 'pytest'],
    test_suite="test",
    cmdclass = {'test': Tox},
    zip_safe=False,
    keywords='Counter ChainMap stuf attribute mapping nested',
    classifiers=linelist("""
        Development Status :: 4 - Beta
        Operating System :: OS Independent
        License :: OSI Approved :: Apache Software License
        Intended Audience :: Developers
        Programming Language :: Python
        Programming Language :: Python :: 2
        Programming Language :: Python :: 2.6
        Programming Language :: Python :: 2.7
        Programming Language :: Python :: 3
        Programming Language :: Python :: 3.2
        Programming Language :: Python :: 3.3
        Programming Language :: Python :: 3.4
        Programming Language :: Python :: 3.5
        Programming Language :: Python :: Implementation :: CPython
        Programming Language :: Python :: Implementation :: PyPy
        Topic :: Software Development :: Libraries :: Python Modules
    """)
)
