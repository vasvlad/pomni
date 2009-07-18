#!/usr/bin/python -tt
# vim: sw=4 ts=4 expandtab ai
#
# Mnemosyne. Learning tool based on spaced repetition technique
#
# Copyright (C) 2008 Pomni Development Team <pomni@googlegroups.com>
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by the
# Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
# 02110-1301 USA
#

"""
Description of the module
"""

import types


def add(int1, int2):
    """ Return sum of two integer numbers
    >>> add(1,2)
    3
    >>> add(2, 3)
    5
    >>> add(0xa, 6)
    16
    >>> add(1.0, 2)
    Traceback (most recent call last):
    ...
    TypeError: Only integer numbers are allowed!
    """
    if type(int2) != types.IntType or type(int1) != types.IntType:
        raise TypeError("Only integer numbers are allowed!")
    return int1 + int2


def _test():
    """ Run doctests
    """
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()

# Local Variables:
# mode: python
# py-indent-offset: 4
# indent-tabs-mode nil
# tab-width 4
# End:
