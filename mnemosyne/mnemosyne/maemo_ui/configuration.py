#!/usr/bin/python -tt7
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
Hildon UI. Configuration Widget.
"""

import os
import gettext
import tts
_ = gettext.gettext

#from mnemosyne.libmnemosyne.ui_component import UiComponent
from mnemosyne.libmnemosyne.ui_components.dialogs import ConfigurationDialog

class ConfigurationWidget(ConfigurationDialog):
    """Configuration Widget."""

    def __init__(self, component_manager):
        ConfigurationDialog.__init__(self, component_manager)

        self.w_tree = self.main_widget().w_tree
        self.w_tree.signal_autoconnect(\
            dict([(sig, getattr(self, sig + "_cb")) for sig in 
                ('change_fullscreen', 'change_font_size', \
                'change_startup_with_review', 'config_to_main_menu', \
                'show_general_settings', 'show_tts_settings', 'change_voice', \
                'change_speed', 'change_pitch')]))
        self.w_tree.get_widget(\
            "config_mode_settings_switcher").set_current_page(0)
        self.w_tree.get_widget("config_toolbar_tts_settings_button")\
            .set_sensitive(tts.is_available())
        #self.conf = self.config()

    def activate(self):
        """Activate configuration mode."""

        self.w_tree.get_widget("checkbox_fullscreen_mode"). \
            set_active(self.config()['fullscreen'])
        self.w_tree.get_widget("checkbox_start_in_review_mode"). \
            set_active(self.config()['startup_with_review'])
        self.current_size = int(self.config()['font_size'])
        self.change_font_size()
        self.w_tree.get_widget("config_mode_entry_imagedir"). \
            set_text(self.config()['imagedir'])
        self.w_tree.get_widget("config_mode_entry_sounddir"). \
            set_text(self.config()['sounddir'])
        self.w_tree.get_widget("config_mode_tts_voice_label"). \
            set_text(self.config()['tts_voice'])
        self.w_tree.get_widget("config_mode_tts_speed_scrollbar"). \
            set_value(self.config()['tts_speed'])
        self.change_speed_cb(self.w_tree.get_widget(\
            "config_mode_tts_speed_scrollbar"))
        self.w_tree.get_widget("config_mode_tts_pitch_scrollbar"). \
            set_value(self.config()['tts_pitch'])
        self.change_pitch_cb(self.w_tree.get_widget(\
            "config_mode_tts_pitch_scrollbar"))

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
    def show_general_settings_cb(self, widget):
        """Switches to the general settings page."""

        self.w_tree.get_widget(\
            "config_mode_settings_switcher").set_current_page(0)
        
    def show_tts_settings_cb(self, widget):
        """Switches to the tts settings page."""

        self.w_tree.get_widget(\
            "config_mode_settings_switcher").set_current_page(1)

    def change_voice_cb(self, widget):
        """Changes TTS voice."""

        voices = {'Male': 'Female', 'Female': 'Male'}
        voice_label = self.w_tree.get_widget("config_mode_tts_voice_label")
        voice = voice_label.get_text()
        voice_label.set_text(voices[voice])
        self.config()['tts_voice'] = voices[voice]

    def change_speed_cb(self, widget):
        """Changes TTS speed."""

        value = int(widget.get_value())
        self.w_tree.get_widget("config_mode_tts_speed_label"). \
            set_text("Speed: %s" % value)

    def change_pitch_cb(self, widget):
        """Changes TTS pitch."""

        value = int(widget.get_value())
        self.w_tree.get_widget("config_mode_tts_pitch_label"). \
            set_text("Pitch: %s" % value)

    def change_fullscreen_cb(self, widget):
        """Change Fullscreen parameter."""

        self.config()['fullscreen'] = \
            self.w_tree.get_widget("checkbox_fullscreen_mode").get_active()

    def change_startup_with_review_cb(self, widget):
        """Change 'Startup with Review' parameter."""

        self.config()['startup_with_review'] = \
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
        self.config()['font_size'] = self.current_size

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
        self.config()['imagedir'] = \
            self.w_tree.get_widget("config_mode_entry_imagedir").get_text()
        self.config()['sounddir'] = \
            self.w_tree.get_widget("config_mode_entry_sounddir").get_text()
        self.config()['tts_speed'] = int(self.w_tree.get_widget(\
            "config_mode_tts_speed_scrollbar").get_value())
        self.config()['tts_pitch'] = int(self.w_tree.get_widget(\
            "config_mode_tts_pitch_scrollbar").get_value())

        #self.config()['font_size'] = self.conf['font_size']
        self.config().save()
        self.main_widget().menu_()


# Local Variables:
# mode: python
# py-indent-offset: 4
# indent-tabs-mode nil
# tab-width 4
# End:
