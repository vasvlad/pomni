#!/usr/bin/python -tt
# vim: sw=4 ts=4 expandtab ai
#
# Pomni. Learning tool based on spaced repetition technique
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
MVC Model
"""

from pomni.patterns import Subject

class ModelException(Exception):
    """ Model Exception """
    pass

class Model(Subject):
    """ MVC pattern. Model - manage state of
    the system and its logic. Doesn't know anything
    about view(s) and controller(s). Communicates with the
    outside word by sending notification events when its
    state is changed. Uses Observer pattern for notifications.
    Has interface methods, which are used by controller and view.
    """

    def __init__(self, database, scheduler):
        """ Constructor """

        Subject.__init__(self)

        self.database, self.scheduler = database, scheduler
        self.learn_ahead = False


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
