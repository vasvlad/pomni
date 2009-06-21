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
Hildon UI
"""

import gettext
_ = gettext.gettext

from mnemosyne.libmnemosyne.component_manager import config, ui_controller_main
from pomni.hildon_ui import HildonBaseController
import os

class HildonUiControllerConfigure(HildonBaseController):
    """ Hildon Config controller """

    def __init__(self, w_tree):
        """Initialization items of config window."""

        HildonBaseController.__init__(self, w_tree)
        signals = ['change_fullscreen', 'change_font_size', \
            'change_startup_with_review', 'change_theme', 'config_to_main_menu']
        self.w_tree.signal_autoconnect(\
            dict([(sig, getattr(self, sig + "_cb")) for sig in signals]))
        self.modified = False
        self.theme_modified = False
        self.configuration = config()

    def activate(self):
        """Start config window."""

        self.checkbox_fullscreen_mode.set_active(
            self.configuration['fullscreen'])
        self.checkbox_start_in_review_mode.set_active(
            self.configuration['startup_with_review'])
        self.font_size_slider.set_value(self.configuration['font_size'])
        self.label_text_size.set_text("Font size: " + \
            self.font_size_slider.get_value().__int__().__str__())
        theme = self.configuration['theme_path'].split("/")[-1]
        self.config_mode_label_theme.set_text("Current theme: " + \
            theme.capitalize())
        self.config_mode_entry_imagedir.set_text(config()['imagedir'])
        self.switcher.set_current_page(self.config)

    def change_fullscreen_cb(self, widget):
        """ Change Fullscreen parameter. """

        self.modified = True
        self.configuration['fullscreen'] = \
            self.checkbox_fullscreen_mode.get_active()

    def change_font_size_cb(self, widget, param1, param2):
        """ Change Font size parameter. """

        self.modified = True
        value = self.font_size_slider.get_value()
        self.configuration['font_size'] = value
        self.label_text_size.set_text("Font size: " + \
            value.__int__().__str__())

    def change_startup_with_review_cb(self, widget):
        """ Change 'Startup with Review' parameter. """

        self.modified = True
        self.configuration['startup_with_review'] = \
            self.checkbox_start_in_review_mode.get_active()

    def change_theme_cb(self, widget):
        """ Change current theme. """

        self.theme_modified = True
        path_list = self.configuration["theme_path"].split("/")
        current_theme = path_list.pop()
        themes = self.configuration["themes"]
        theme_index = themes.index(current_theme)
        try:
            new_theme = themes[theme_index + 1]
        except IndexError:
            new_theme = themes[0]
        path_list.append(new_theme)
        self.configuration["theme_path"] = "/".join(path_list)
        self.config_mode_label_theme.set_text(\
            "New theme: " + new_theme.capitalize())
        self.configuration.save()

    def config_to_main_menu_cb(self, widget):
        """ Return to main menu. """

        if self.modified:
            self.configuration.save()
        if self.theme_modified:
            ui_controller_main().widget.information_box(\
                _("Restart the program to take effect!"), "OK")
        if not os.path.exists(self.config_mode_entry_imagedir.get_text()):
            ui_controller_main().widget.information_box(\
                _("Image dir does not exist! Select another."), "OK")
            return
        else:
            self.configuration['imagedir'] = self.config_mode_entry_imagedir.get_text()
            self.configuration.save()
        self.switcher.set_current_page(self.main_menu)

EternalControllerConfigure = HildonUiControllerConfigure
RainbowControllerConfigure = HildonUiControllerConfigure


# Local Variables:
# mode: python
# py-indent-offset: 4
# indent-tabs-mode nil
# tab-width 4
# End:
