#!/usr/bin/env python

import glob
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

package_name = open('debian/changelog').readline().split(' ')[0]

setup(name = package_name,
    description='Learning tool based on spaced repetition technique',
    version = open('debian/changelog').readline().split(' ')[1][1:-1],
    author = "Pomni Development team",
    author_email = "pomni@googlegroups.com",
    license='GPL 2',
    packages = ["pomni"],
    package_dir = {'pomni': ''},
    data_files=[('share/%s/UI' % package_name, glob.glob('UI/*')), 
                ('share/%s/hildon-UI/draft' % package_name,  glob.glob('hildon-UI/draft/*')),
		('share/%s/hildon-UI/eternal' % package_name,  glob.glob('hildon-UI/eternal/*')),
		('share/dbus-1/services', ['maemo/%s.service' % package_name]),
		('share/applications/hildon', ['maemo/%s.desktop' % package_name])],
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

