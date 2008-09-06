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
Factory. Creates objects
"""

from mnemosyne.libmnemosyne.databases.pickle import Pickle

from pomni.cmd_ui import CommandlineUI
from pomni.dummy_backend import DummyBackend

def ui_factory(model, interface=None):
    """ Create UI(View in terms of MVC) """

    if not interface:
        # default UI
        return CommandlineUI(model)

    if interface == "cmd":
        return CommandlineUI(model)
    elif interface == "hildon":
        raise NotImplementedError("Hildon UI is not implemented yet.")
    # add next gui here

    raise ValueError("No idea how to create %s UI" % interface)


def backend_factory(name=None):
    """ Create backend """

    if not name or name == 'dummy':
        return DummyBackend()
    if name == 'pickle':
        return Pickle()

    raise ValueError("No idea how to create %s backend" % name)


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
