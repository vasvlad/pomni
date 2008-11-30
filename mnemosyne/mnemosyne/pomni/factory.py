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
UI Factory. Creates UI objects
"""

from mnemosyne.libmnemosyne.databases.pickle import Pickle
from mnemosyne.libmnemosyne.component_manager import component_manager
from mnemosyne.libmnemosyne.renderers.text import TextRenderer

def ui_factory(model, interface=None):
    """ Create UI(View in terms of MVC) """

    if interface == 'cmd':
        # default UI
        from pomni.cmd_ui import CmdUiControllerReview, CmdReviewWdgt, CommandlineUI

        component_manager.register("ui_controller_review", CmdUiControllerReview())
        component_manager.register("review_widget", CmdReviewWdgt)
        component_manager.register("renderer", TextRenderer())
        return CommandlineUI(model)

    if not interface or interface == "hildon":
        from pomni.hildon_ui import HildonUiControllerReview, HildonReviewWdgt, HildonUI

        component_manager.register("ui_controller_review", HildonUiControllerReview())
        component_manager.register("review_widget", HildonReviewWdgt)
        component_manager.register("renderer", TextRenderer())
        return HildonUI(model)
    
    # add next gui here
    raise ValueError("No idea how to create %s UI" % interface)

def backend_factory(name=None):
    """ Create backend """

    if not name or name == "pickle":
    	return Pickle()
    if name == 'sqlite':
        raise NotImplementedError("SQLite backend is not implemented yet")

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
