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
Dummy Backend
"""


class DummyBackend:
    """ Dummy backend """

    def __init__(self):
        self.records = {"word1": {"back": "translation1", "mark": 0},
                        "word2": {"back": "translation2", "mark": 1},
                        "word3": {"back": "translation3", "mark": 2}}

    def get_list(self, sort=False):
        """ Get list of records' names from the storage """
        keys = self.records.keys()
        if sort:
            keys = sorted(keys)
        return keys

    def get_record(self, name):
        """ Get record by name """

        return self.records[name]

    def set_field(self, name, key, val):
        """ Set field value """

        self.records[name][key] = val

    def add_field(self, name, back):
        """ Add new record """

        self.records[name] = {"back": back, "mark": 0}

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
