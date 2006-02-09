#!/usr/bin/env python

VERSION = '0.1'

long_description = """
gtktest is a collection of helpers that wrap pyGTK to make it
easy to test.  It allows testing of modal dialogs and recursive
mainloop invocations while preventing the windows from being shown
during test runs.  Arbitrary classes and methods can be overriden
or call loggers can be attached to them.
"""

classifiers = ["Development Status :: 4 - Beta",
               "Intended Audience :: Developers",
               "License :: OSI Approved :: MIT License",
               "Operating System :: POSIX",
               "Programming Language :: Python",
               "Topic :: Software Development :: Testing"]


import distutils.core


def main():
    distutils.core.setup(
            name='gtktest',
            version=VERSION,
            description='library of helpers for unit-testing GTK applications',
            long_description=long_description,
            classifiers=classifiers,
            url='http://gintas.pov.lt/gtktest',
            data_files=[('share/doc/python-gtktest', ['README', 'LICENSE'])],
            packages=['gtktest'],
            author="Gintautas Miliauskas",
            author_email="gintas@pov.lt",
            platforms='POSIX',
            license="MIT",
            )


if __name__ == '__main__':
    main()
