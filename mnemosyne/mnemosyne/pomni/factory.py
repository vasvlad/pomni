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

from mnemosyne.libmnemosyne import Mnemosyne
from mnemosyne.libmnemosyne.component import Component

class ConfigHook(Component):
    """Configuration hook."""
    component_type = 'hook'
    used_for = 'configuration_defaults'

    def run(self):
        """Entry point."""
        for key, value in {\
            "theme_path": "/usr/share/pomni/hildon-UI/rainbow",
            "themes": ['rainbow'],
            "fullscreen": True,
            "font_size": 30.0,
            "startup_with_review": False,
            "upload_logs": False,
            "imagedir": "/home/user/MyDocs/.images",
            "sounddir": "/home/user/MyDocs/.sounds",
            "times_loaded": 0}.iteritems():

            self.config().setdefault(key, value)

def app_factory(interface=None):
    """Mnemosyne application factory."""

    app = Mnemosyne()
    app.components.append(("pomni.factory", "ConfigHook"))

    if interface == 'cmd':
        #from pomni.cmd_ui import CmdUiControllerReview, CommandlineUI

        #component_manager.register("ui_controller_review",
        #                           CmdUiControllerReview())
        #component_manager.register("renderer", TextRenderer())
        raise NotImplementedError('cmd ui has to be redesigned')

    if not interface or interface == "hildon":
        app.components.insert(0, ("mnemosyne.libmnemosyne.translator",
                                  "GetTextTranslator"))
        app.components.append(("pomni.renderers", "Html"))
        app.components.append(("pomni.main", "HildonMainWidget"))
        app.components.append(\
            ("mnemosyne.libmnemosyne.ui_components.review_widget",
             "ReviewWidget"))

        # Add necessary components
        app.components.append(\
            ("mnemosyne.libmnemosyne.card_types.cloze", "Cloze"))

        # Remove unused components
        app.components.remove(\
            ("mnemosyne.libmnemosyne.card_types.map", "MapPlugin"))
        app.components.remove(\
            ("mnemosyne.libmnemosyne.card_types.cloze", "ClozePlugin"))
        app.components.remove(\
            ("mnemosyne.libmnemosyne.plugins.cramming_plugin", \
                "CrammingPlugin"))
        app.components.remove(\
            ("mnemosyne.libmnemosyne.renderers.html_css", "HtmlCss"))
        app.components.remove(\
            ("mnemosyne.libmnemosyne.filters.escape_to_html", "EscapeToHtml"))
        app.components.remove(\
            ("mnemosyne.libmnemosyne.filters.expand_paths", "ExpandPaths"))
        app.components.remove(\
            ("mnemosyne.libmnemosyne.filters.latex", "Latex"))
        return app

    # add next gui here
    raise ValueError("No idea how to create %s app" % interface)


# Local Variables:
# mode: python
# py-indent-offset: 4
# indent-tabs-mode nil
# tab-width 4
# End:
