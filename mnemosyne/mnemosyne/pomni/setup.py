#!/usr/bin/python -tt

""" Setup """

import glob
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

PKG = open('debian/changelog').readline().split(' ')[0]

setup(name=PKG,
    description='Learning tool based on spaced repetition technique',
    version=open('debian/changelog').readline().split(' ')[1][1:-1],
    author="Pomni Development team",
    author_email="pomni@googlegroups.com",
    license='GPL 2',
    packages=["pomni"],
    package_dir={'pomni': ''},
    data_files=[\
        ('share/%s/hildon-UI/draft' % PKG, glob.glob('hildon-UI/draft/*')),
        ('share/%s/hildon-UI/eternal' % PKG, glob.glob('hildon-UI/eternal/*')),
        ('share/%s/hildon-UI/smile' % PKG, glob.glob('hildon-UI/smile/*')),
        ('share/dbus-1/services', ['maemo/%s.service' % PKG]),
        ('share/applications/hildon', ['maemo/%s.desktop' % PKG])],
    classifiers=[
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License (GPL)',
    'Natural Language :: English',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries',
    ])
