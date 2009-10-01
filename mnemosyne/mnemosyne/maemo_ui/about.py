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
Hildon UI. About Widget.
"""

import os
from mnemosyne.libmnemosyne.ui_component import UiComponent


class AboutWidget(UiComponent):
    """About Widget."""

    def __init__(self, component_manager):
        UiComponent.__init__(self, component_manager)
        w_tree = self.main_widget().w_tree
        w_tree.signal_autoconnect(dict([(sig, getattr(self, sig + "_cb")) \
            for sig in ('about_to_main_menu', 'show_team_info', 'show_guide')]))
        self.get_widget = w_tree.get_widget
        self.conf = self.config()
        self.renderer = self.component_manager.get_current('renderer')
        if self.config()['last_about_page'] == 0:
            self.show_team_info_cb(None)
        else:
            self.show_guide_cb(None)

    def show_team_info_cb(self, widget):
        """Show team info page."""

        self.get_widget("about_mode_role_switcher").set_current_page(0)
        self.get_widget("about_toolbar_team_button").set_active(True)
        self.get_widget("about_mode_logo_image").set_from_file(\
            os.path.join(self.conf['theme_path'], "mnemosyne.png"))

    def show_guide_cb(self, widget):
        """Show user guide page."""

        #FIXME: load from html-file
        self.renderer.render_html(self.get_widget("about_mode_guide_text"), \
            "<html><b>Mnemosyne for Maemo user guide</b></html>")
        self.get_widget("about_mode_role_switcher").set_current_page(1)
        self.get_widget("about_toolbar_guide_button").set_active(True)

    def about_to_main_menu_cb(self, widget):
        """Returns to main menu."""

        self.conf['last_about_page'] = self.get_widget(\
            "about_mode_role_switcher").get_current_page()
        self.conf.save()
        self.main_widget().menu_()
       
