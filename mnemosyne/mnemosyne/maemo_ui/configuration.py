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
        self.get_widget = self.w_tree.get_widget
        self.conf = self.config()
        self.current_size = int(self.conf['font_size'])
        self.change_font_size()
        self.connections = []
        self.connect_signals([
            ("checkbox_fullscreen_mode", "toggled", self.change_fullscreen_cb),
            ("checkbox_start_in_review_mode", "toggled", \
                self.change_startup_with_review_cb),
            ("config_mode_decrease_font_size_buttton", "button-press-event", \
                self.change_font_size_cb),
            ("config_mode_increase_font_size_buttton", "button-press-event", \
                self.change_font_size_cb),
            ("config_toolbar_main_menu_button", "button-press-event", \
                self.config_to_main_menu_cb),
            ("config_toolbar_general_settings_button", "clicked", \
                self.show_general_settings_cb),
            ("config_toolbar_tts_settings_button", "clicked", \
                self.show_tts_settings_cb),
            ("config_mode_tts_voice_prev_button", "button-press-event", \
                self.change_voice_cb),
            ("config_mode_tts_voice_next_button", "button-press-event", \
                self.change_voice_cb),
            ("config_mode_tts_speed_scrollbar", "value-changed", \
                self.change_speed_cb),
            ("config_mode_tts_pitch_scrollbar", "value-changed", \
                self.change_pitch_cb),
            ("config_mode_tts_lang_prev_button", "button-press-event", \
                self.change_lang_cb),
            ("config_mode_tts_lang_next_button", "button-press-event", \
                self.change_lang_cb)])

        self.get_widget("config_mode_settings_switcher"). \
            set_current_page(self.conf['last_settings_page'])
        tts_available = tts.is_available()
        self.get_widget("config_toolbar_tts_settings_button").set_sensitive(\
            tts_available)
        if tts_available:
            self.languages = [lang for lang in tts.get_languages()]

    def connect_signals(self, control):
        """Connect signals to widgets and save connection info."""

        for wname, signal, callback in control:
            widget = self.get_widget(wname)
            cid = widget.connect(signal, callback)
            self.connections.append((widget, cid))

    def disconnect_signals(self):
        """Disconnect previously connected signals."""

        for widget, cid in self.connections:
            widget.disconnect(cid)
        self.connections = []

    def activate(self):
        """Activate configuration mode."""

        self.get_widget("checkbox_fullscreen_mode").set_active(\
            self.conf['fullscreen'])
        self.get_widget("checkbox_start_in_review_mode").set_active(\
            self.conf['startup_with_review'])
        self.get_widget("config_mode_entry_imagedir").set_text(\
            self.conf['imagedir'])
        self.get_widget("config_mode_entry_sounddir").set_text(\
            self.conf['sounddir'])
        self.get_widget("config_mode_tts_voice_label").set_text(\
            self.conf['tts_voice'])
        self.get_widget("config_mode_tts_speed_scrollbar").set_value(\
            self.conf['tts_speed'])
        self.change_speed_cb(self.get_widget("config_mode_tts_speed_scrollbar"))
        self.get_widget("config_mode_tts_pitch_scrollbar").set_value(\
            self.conf['tts_pitch'])
        self.change_pitch_cb(self.get_widget("config_mode_tts_pitch_scrollbar"))
        self.get_widget("config_mode_tts_lang_label").set_text(\
            self.conf['tts_language'])

    def change_font_size(self):
        """Changes font size."""

        document = self.get_widget("font_size_example").document
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

        self.get_widget("config_mode_settings_switcher").set_current_page(0)
        
    def show_tts_settings_cb(self, widget):
        """Switches to the tts settings page."""

        self.get_widget("config_mode_settings_switcher").set_current_page(1)

    def change_voice_cb(self, widget, event):
        """Changes TTS voice."""

        voices = {'Male': 'Female', 'Female': 'Male'}
        voice_label = self.get_widget("config_mode_tts_voice_label")
        voice = voice_label.get_text()
        voice_label.set_text(voices[voice])

    def change_lang_cb(self, widget, event):
        """Changes current TTS language."""

        lang_index = self.languages.index(\
            self.get_widget("config_mode_tts_lang_label").get_text())
        direction = 1
        if widget == self.get_widget("config_mode_tts_lang_prev_button"):
            direction = -1
        try:
            new_lang = self.languages[lang_index + direction]
        except IndexError:
            if direction:
                new_lang = self.languages[0]
            else:
                new_lang = self.languages[-1]
        finally:
            self.get_widget("config_mode_tts_lang_label").set_text(new_lang)

    def change_speed_cb(self, widget):
        """Changes TTS speed."""

        value = int(widget.get_value())
        self.get_widget("config_mode_tts_speed_label").set_text(\
            "    Speed: %s" % value)

    def change_pitch_cb(self, widget):
        """Changes TTS pitch."""

        value = int(widget.get_value())
        self.get_widget("config_mode_tts_pitch_label").set_text(\
            "    Pitch: %s" % value)

    def change_fullscreen_cb(self, widget):
        """Change Fullscreen parameter."""

        self.conf['fullscreen'] = self.get_widget(\
            "checkbox_fullscreen_mode").get_active()

    def change_startup_with_review_cb(self, widget):
        """Change 'Startup with Review' parameter."""

        self.conf['startup_with_review'] = self.get_widget(\
            "checkbox_start_in_review_mode").get_active()

    def change_font_size_cb(self, widget, event):
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

    def config_to_main_menu_cb(self, widget, event):
        """ Return to main menu. """

        if not os.path.exists( \
            self.get_widget("config_mode_entry_imagedir").get_text()):
            self.main_widget().information_box( \
                _("Image dir does not exist! Select another."))
            return
        if not os.path.exists( \
            self.get_widget("config_mode_entry_sounddir").get_text()):
            self.main_widget().information_box( \
                _("Sound dir does not exist! Select another."))
            return
        self.conf['imagedir'] = self.get_widget(\
            "config_mode_entry_imagedir").get_text()
        self.conf['sounddir'] = self.get_widget(\
            "config_mode_entry_sounddir").get_text()
        self.conf['tts_speed'] = int(self.get_widget(\
            "config_mode_tts_speed_scrollbar").get_value())
        self.conf['tts_pitch'] = int(self.get_widget(\
            "config_mode_tts_pitch_scrollbar").get_value())
        self.conf['tts_language'] = self.get_widget(\
            "config_mode_tts_lang_label").get_text()
        self.conf['tts_voice'] = self.get_widget(\
            "config_mode_tts_voice_label").get_text()
        self.conf['last_settings_page'] = self.get_widget(\
            "config_mode_settings_switcher").get_current_page()
        self.conf.save()
        self.disconnect_signals()
        self.main_widget().menu_()


# Local Variables:
# mode: python
# py-indent-offset: 4
# indent-tabs-mode nil
# tab-width 4
# End:
