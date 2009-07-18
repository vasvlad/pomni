#!/usr/bin/python -tt

""" Setup """

import os
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
    packages=["mnemosyne"],
    package_dir={'mnemosyne': ''},
    data_files = [(os.path.join('share/%s/' % PKG, path), \
        [os.path.join(path, fname) for fname in files]) \
        for path, dirs, files in os.walk('hildon-UI/eternal')] + \
        [(os.path.join('share/%s/' % PKG, path), \
        [os.path.join(path, fname) for fname in files]) \
        for path, dirs, files in os.walk('hildon-UI/rainbow')] + \
       [('share/dbus-1/services', ['maemo/%s.service' % PKG]),
        ('share/applications/hildon', ['maemo/%s.desktop' % PKG]),
        ('share/%s/demo' % PKG, [".%s/default.db" % PKG]),
        ('share/icons/hicolor/26x26/apps/', ['./maemo/icons/26x26/mnemosyne.png']),
        ('share/icons/hicolor/64x64/apps/', ['./maemo/icons/64x64/mnemosyne.png'])],
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
