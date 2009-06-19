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

#from mnemosyne.libmnemosyne.renderers.html_hildon import HtmlHildon
#from mnemosyne.libmnemosyne.renderers.text import TextRenderer

from mnemosyne.libmnemosyne import Mnemosyne
from mnemosyne.libmnemosyne.component import Component

class ConfigHook(Component):
    component_type = 'hook'
    used_for = 'configuration_defaults'

    def run(self):
        try:
            for key, value in {\
                "theme_path": "/usr/share/pomni/hildon-UI/eternal",
                "themes": ['eternal', 'rainbow'],
                "scheduler": "SM2",
                "database": "sqlite",
                "fullscreen": True,
                "font_size": 30.0,
                "startup_with_review": False,
                "times_loaded": 0}.iteritems():

                self.config().setdefault(key, value)

            print ">>>>", self.config()['theme_path']
        except Exception, exobj:
            print '>>>>>Exception:', exobj

def app_factory(interface=None):
    """UI factory. Return main ui object."""

    app = Mnemosyne()
    app.components.append(("pomni.factory", "ConfigHook"))

    if interface == 'cmd':
        from pomni.cmd_ui import CmdUiControllerReview, CommandlineUI

        component_manager.register("ui_controller_review",
                                   CmdUiControllerReview())
        component_manager.register("renderer", TextRenderer())
        return CommandlineUI()

    if not interface or interface == "hildon":
        # FIXME: get current theme here

        app.components.insert(0, ("mnemosyne.libmnemosyne.translator",
                                  "GetTextTranslator"))

        app.components.append(("pomni.main", "HildonMainWidget"))
        app.components.append(("pomni.review", "HildonReviewWidget"))

        return app

    # add next gui here
    raise ValueError("No idea how to create %s app" % interface)


# Local Variables:
# mode: python
# py-indent-offset: 4
# indent-tabs-mode nil
# tab-width 4
# End:
