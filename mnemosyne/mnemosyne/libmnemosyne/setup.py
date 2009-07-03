#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name = "libmnemosyne",
    description='Mnemosyne core library',
    version = open('debian/changelog').readline().split(' ')[1][1:-1],
    author = "Peter Bienstman",
    author_email = "Peter.Bienstman@UGent.be",
    license='GPL 2',
    packages = [ "mnemosyne.libmnemosyne"] + ["mnemosyne.libmnemosyne.%s" \
        % pkg for pkg in ["card_types", "databases", "file_formats", "filters",
        "loggers", "plugins", "renderers", "schedulers", "statistics_pages", 
        "ui_controllers_main", "ui_controllers_review"]
    ],
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

