#!/usr/bin/python -tt7
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
Hildon UI. Configuration Widget.
"""

import os
import gettext
_ = gettext.gettext

from mnemosyne.libmnemosyne.ui_component import UiComponent

class RainbowConfigurationWidget(UiComponent):
    """Configuration Widget."""

    def __init__(self, component_manager):
        UiComponent.__init__(self, component_manager)

        self.w_tree = self.main_widget().w_tree
        self.w_tree.signal_autoconnect(\
            dict([(sig, getattr(self, sig + "_cb")) for sig in 
                ('change_fullscreen', 'change_font_size', \
                'change_startup_with_review', 'config_to_main_menu')]))
        self.conf = self.config()

    def activate(self):
        """Activate configuration mode."""

        self.w_tree.get_widget("checkbox_fullscreen_mode"). \
            set_active(self.conf['fullscreen'])
        self.w_tree.get_widget("checkbox_start_in_review_mode"). \
            set_active(self.conf['startup_with_review'])
        self.current_size = int(self.conf['font_size'])
        self.change_font_size()
        self.w_tree.get_widget("config_mode_entry_imagedir"). \
            set_text(self.conf['imagedir'])
        self.w_tree.get_widget("config_mode_entry_sounddir"). \
            set_text(self.conf['sounddir'])

    def change_font_size(self):
        """Changes font size."""

        document = self.w_tree.get_widget("font_size_example").document
        document.clear()
        document.open_stream('text/html')
        text = """<html><style type="text/css"> *{font-size:%spx; \
            text-align:center;}</style><body>Font size example \
            </body></html>""" % self.current_size
        document.write_stream(text)
        document.close_stream()

    # callbacks
    def change_fullscreen_cb(self, widget):
        """Change Fullscreen parameter."""

        self.conf['fullscreen'] = \
            self.w_tree.get_widget("checkbox_fullscreen_mode").get_active()

    def change_startup_with_review_cb(self, widget):
        """Change 'Startup with Review' parameter."""

        self.conf['startup_with_review'] = \
            self.w_tree.get_widget("checkbox_start_in_review_mode").get_active()

    def change_font_size_cb(self, widget):
        """Change Font size parameter."""

        # move to config?
        min_size = 10
        max_size = 60
        if widget.name == "config_mode_decrease_font_size_buttton":
            if self.current_size > min_size:
                self.current_size -= 1
        else:
            if self.current_size < max_size:
                self.current_size += 1
        self.change_font_size()
        self.conf['font_size'] = self.current_size

    def config_to_main_menu_cb(self, widget):
        """ Return to main menu. """

        if not os.path.exists( \
            self.w_tree.get_widget("config_mode_entry_imagedir").get_text()):
            self.main_widget().information_box( \
                _("Image dir does not exist! Select another."))
            return
        if not os.path.exists( \
            self.w_tree.get_widget("config_mode_entry_sounddir").get_text()):
            self.main_widget().information_box( \
                _("Sound dir does not exist! Select another."))
            return
        self.conf['imagedir'] = \
            self.w_tree.get_widget("config_mode_entry_imagedir").get_text()
        self.conf['sounddir'] = \
            self.w_tree.get_widget("config_mode_entry_sounddir").get_text()
        self.conf.save()
        self.main_widget().activate_mode("menu")


# Local Variables:
# mode: python
# py-indent-offset: 4
# indent-tabs-mode nil
# tab-width 4
# End:
