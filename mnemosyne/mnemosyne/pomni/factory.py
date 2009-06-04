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

from mnemosyne.libmnemosyne.renderers.html_hildon import HtmlHildon
from mnemosyne.libmnemosyne.renderers.text import TextRenderer

from mnemosyne.libmnemosyne import Mnemosyne

from mnemosyne.libmnemosyne.ui_components.review_widget import ReviewWidget

class FakeControllerReview(ReviewWidget):
    """ Hildon Review controller """

    def activate(self):
        pass

class App(Mnemosyne):
    def __init__(self, resource_limited=False):
        Mnemosyne.__init__(self, resource_limited)
        self.components.insert(0, ("mnemosyne.libmnemosyne.translator",
             "GetTextTranslator"))

    def initialise(self, basedir, filename=None):
        Mnemosyne.initialise(self, basedir, filename=None)

def ui_factory(basedir, interface=None):
    """UI factory. Return main ui object."""

    app = App()

    if interface == 'cmd':
        from pomni.cmd_ui import CmdUiControllerReview, CommandlineUI

        component_manager.register("ui_controller_review",
                                   CmdUiControllerReview())
        component_manager.register("renderer", TextRenderer())
        return CommandlineUI()

    if not interface or interface == "hildon":
        # FIXME: get current theme here

        app.components.append(("pomni.hildon_ui", "HildonUI"))
        app.components.append(("pomni.factory",
                               "FakeControllerReview"))
        print 'before initialise'
        app.initialise(basedir)

        print '>>> main-widget=', app.main_widget()

        return app.main_widget()

    # add next gui here
    raise ValueError("No idea how to create %s UI" % interface)


# Local Variables:
# mode: python
# py-indent-offset: 4
# indent-tabs-mode nil
# tab-width 4
# End:
