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

import types

from pomni.patterns import Subject


class Model(Subject):
    """ MVC pattern. Model - manage state of
    the system and its logic. Doesn't know anything
    about view(s) and controller(s). Communicates with the
    outside word by sending notification events when its
    state is changed. Uses Observer pattern for notifications.
    Has interface methods, which are used by controller and view.
    """

    class ModelException(Exception):
        """ Model Exception """
        pass

    def __init__(self, backend):
        """ Constructor """

        Subject.__init__(self)

        self.backend = backend

    def scheduled(self):
        """ Return next scheduled card """
        for name in self.backend.get_list(sort=True):
            yield (name, self.backend.get_record(name))

    def is_valid_mark(self, mark):
        """ Check if mark is valid """

        if type(mark) != types.IntType or not 0 <= mark <= 5:
            raise self.ModelException(\
                "Error: Mark has to be a number from 0 to 5")
        return True

    def update_mark(self, name, mark):
        """ Update the card's mark """

        if not mark.isdigit():
            raise self.ModelException("Error: Mark has to be a number")

        mark = int(mark)
        if self.is_valid_mark(mark):
            self.backend.set_field(name, "mark", mark)
            self.notify()


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
