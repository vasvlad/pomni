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
import gtk
_ = gettext.gettext

from mnemosyne.maemo_ui.widgets import BaseHildonWidget
from mnemosyne.libmnemosyne.ui_components.dialogs import ConfigurationDialog

class ConfigurationWidget(BaseHildonWidget, ConfigurationDialog):
    """Configuration Widget."""

    def __init__(self, component_manager):
        ConfigurationDialog.__init__(self, component_manager)
        BaseHildonWidget.__init__(self, component_manager)
        self.current_size = self.conf['font_size']
        self.languages = []
        self.renderer = self.component_manager.get_current('renderer')
        page = self.conf['last_settings_page']
        get_widget = self.get_widget
        if page == 0:
            get_widget("config_toolbar_general_settings_button").\
                set_active(True)
            self.show_general_settings_cb(None)
        elif page == 1:
            get_widget("config_toolbar_skin_settings_button").set_active(True)
            self.show_skin_settings_cb(None)
        elif page == 2 and tts.is_available():
            get_widget("config_toolbar_tts_settings_button").set_active(True)
            self.show_tts_settings_cb(None)
        else:
            get_widget("config_toolbar_general_settings_button").\
                set_active(True)
            get_widget("config_toolbar_tts_settings_button").\
                set_sensitive(False)
            self.show_general_settings_cb(None)

        self.connect_signals([
            ("checkbox_fullscreen_mode", "toggled", self.change_fullscreen_cb),
            ("checkbox_start_in_review_mode", "toggled", \
                self.change_startup_with_review_cb),
            ("config_mode_decrease_font_size_buttton", "clicked", \
                self.change_font_size_cb),
            ("config_mode_increase_font_size_buttton", "clicked", \
                self.change_font_size_cb),
            ("config_toolbar_main_menu_button", "clicked", \
                self.config_to_main_menu_cb),
            ("config_toolbar_general_settings_button", "released", \
                self.show_general_settings_cb),
            ("config_toolbar_skin_settings_button", "released", \
                self.show_skin_settings_cb),
            ("config_toolbar_tts_settings_button", "released", \
                self.show_tts_settings_cb),
            ("config_mode_tts_voice_prev_button", "clicked", \
                self.change_voice_cb),
            ("config_mode_tts_voice_next_button", "clicked", \
                self.change_voice_cb),
            ("config_mode_tts_speed_scrollbar", "value-changed", \
                self.change_speed_cb),
            ("config_mode_tts_pitch_scrollbar", "value-changed", \
                self.change_pitch_cb),
            ("config_mode_tts_lang_prev_button", "clicked", \
                self.change_lang_cb),
            ("config_mode_tts_lang_next_button", "clicked", \
                self.change_lang_cb),
            ("config_mode_prev_skin_button", "clicked", self.change_skin_cb),
            ("config_mode_next_skin_button", "clicked", self.change_skin_cb),
            ("config_mode_entry_imagedir", "changed", \
                self.save_imagedir_value),
            ("config_mode_entry_sounddir", "changed", \
                self.save_sounddir_value)])

    def change_font_size(self):
        """Changes font size."""

        self.renderer.render_html(self.get_widget("font_size_example"), \
            """<html><style type="text/css"> *{font-size:%spx; \
            text-align:center;} body {background:#FFFFFF; color:#000000}\
            </style><body>Font size: %s </body></html>""" % \
            (self.current_size, int(self.current_size)))

    def save_imagedir_value(self, widget):
        """Save current imagedir value."""

        self.conf['imagedir'] = widget.get_text()

    def save_sounddir_value(self, widget):
        """Save current sounddir value."""

        self.conf['sounddir'] = widget.get_text()

    # callbacks
    def show_general_settings_cb(self, widget):
        """Switches to the general settings page."""

        self.get_widget("config_mode_settings_switcher").set_current_page(0)
        self.get_widget("checkbox_fullscreen_mode").set_active(\
            self.conf['fullscreen'])
        self.get_widget("checkbox_start_in_review_mode").set_active(\
            self.conf['startup_with_review'])
        self.get_widget("config_mode_entry_imagedir").set_text(\
            self.conf['imagedir'])
        self.get_widget("config_mode_entry_sounddir").set_text(\
            self.conf['sounddir'])
        
    def show_tts_settings_cb(self, widget):
        """Switches to the tts settings page."""

        self.get_widget("config_mode_settings_switcher").set_current_page(2)
        if not self.languages:
            self.languages = [lang for lang in tts.get_languages()]
        self.get_widget("config_mode_tts_voice_label").set_text(\
            self.conf['tts_voice'])
        self.get_widget("config_mode_tts_lang_label").set_text(\
            self.conf['tts_language'])
        self.get_widget("config_mode_tts_speed_scrollbar").set_value(\
            self.conf['tts_speed'])
        self.get_widget("config_mode_tts_pitch_scrollbar").set_value(\
            self.conf['tts_pitch'])
        self.change_speed_cb(self.get_widget("config_mode_tts_speed_scrollbar"))
        self.change_pitch_cb(self.get_widget("config_mode_tts_pitch_scrollbar"))

    def show_skin_settings_cb(self, widget):
        """Switches to the skin settings page."""

        self.get_widget("config_mode_settings_switcher").set_current_page(1)
        self.change_font_size()
        preview_image = self.get_widget("config_mode_skin_preview_image")
        if not preview_image.get_property('file'):
            preview_image.set_from_file(os.path.join(self.conf["theme_path"], \
            os.path.split(self.conf["theme_path"])[1]))

    def change_voice_cb(self, widget):
        """Changes TTS voice."""

        voices = {'Male': 'Female', 'Female': 'Male'}
        voice_label = self.get_widget("config_mode_tts_voice_label")
        voice = voice_label.get_text()
        new_voice = voices[voice]
        voice_label.set_text(new_voice)
        self.conf['tts_voice'] = new_voice

    def change_lang_cb(self, widget):
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
            self.conf['tts_language'] = new_lang
            self.get_widget("config_mode_tts_lang_label").set_text(new_lang)

    def change_skin_cb(self, widget):
        """Changes current skin."""

        skins = {'rainbow': 'dark', 'dark': 'rainbow'}
        skin_preview_widget = self.get_widget("config_mode_skin_preview_image")
        path, skin = os.path.split(\
            skin_preview_widget.get_properties('file')[0])
        path = os.path.split(path)[0]
        skin_preview_widget.set_from_file(os.path.join(os.path.join(\
            path, skins[skin]), skins[skin]))
        self.conf['theme_path'] = os.path.join(path, skins[skin])

    def change_speed_cb(self, widget):
        """Changes TTS speed."""

        value = int(widget.get_value())
        self.conf['tts_speed'] = value
        self.get_widget("config_mode_tts_speed_label").set_text(\
            "    Speed: %s" % value)

    def change_pitch_cb(self, widget):
        """Changes TTS pitch."""

        value = int(widget.get_value())
        self.conf['tts_pitch'] = value
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

        if not os.path.exists(os.path.abspath(self.get_widget(\
            "config_mode_entry_imagedir").get_text())):
            self.main_widget().information_box(\
                _("Image dir does not exist! Select another."))
            return
        if not os.path.exists(os.path.abspath(self.get_widget(\
            "config_mode_entry_sounddir").get_text())):
            self.main_widget().information_box(\
                _("Sound dir does not exist! Select another."))
            return
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
