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

from mnemosyne.libmnemosyne.component_manager import component_manager
from mnemosyne.libmnemosyne.renderers.html_hildon import HtmlHildon
from mnemosyne.libmnemosyne.renderers.text import TextRenderer

def ui_factory(interface=None):
    """ Create UI(View in terms of MVC) """

    from mnemosyne.libmnemosyne.ui_controllers_main.default_main_controller \
                                               import DefaultMainController
    component_manager.register("ui_controller_main", DefaultMainController())

    if interface == 'cmd':
        from pomni.cmd_ui import CmdUiControllerReview, CommandlineUI

        component_manager.register("ui_controller_review",
                                   CmdUiControllerReview())
        component_manager.register("renderer", TextRenderer())
        return CommandlineUI()

    if not interface or interface == "hildon":
    
        from pomni.hildon_ui import HildonUI
        component_manager.register("renderer", HtmlHildon())
        return HildonUI()

    # add next gui here
    raise ValueError("No idea how to create %s UI" % interface)


if __name__ == "__main__":
    _test()


# Local Variables:
# mode: python
# py-indent-offset: 4
# indent-tabs-mode nil
# tab-width 4
# End:
