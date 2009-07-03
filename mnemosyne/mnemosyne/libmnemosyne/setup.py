#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name = "libmnemosyne",
    description='Mnemosyne core library',
    version = open('debian/changelog').readline().split(' ')[1][1:-1],
    author = "Peter Bienstman",
    author_email = "Peter.Bienstman@UGent.be",
    license='GPL 2',
    packages = [ "mnemosyne.libmnemosyne"] + \
        ["mnemosyne.libmnemosyne.%s" % pkg for pkg in find_packages()],
    package_dir = {'mnemosyne.libmnemosyne': '', 'mnemosyne': 'debian'},
    classifiers = [
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License (GPL)',
    'Natural Language :: English',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries',
    ]
)

