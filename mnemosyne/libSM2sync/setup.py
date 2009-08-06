#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name = "libSM2sync",
    description='Sync library for SM2 schedulers',
    version = open('debian/changelog').readline().split(' ')[1][1:-1],
    author = "users",
    author_email = "mail@gmail.com",
    license='GPL 2',
    packages = [ "mnemosyne.libSM2sync"],
    package_dir = {'mnemosyne.libSM2sync': ''},
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

