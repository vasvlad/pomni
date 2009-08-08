#!/usr/bin/python -tt

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(name="libSM2sync",
    version=open('debian/changelog').readline().split(' ')[1][1:-1],
    description="Sync library for SM2 schedulers",
    author="Max Usachev, Ed Bartosh, Peter Beinstman",
    author_email="pomni@googlegroups.com",
    license="GPL 2",
    packages=["libSM2sync"],
    package_dir={"libSM2sync": ""}
)
