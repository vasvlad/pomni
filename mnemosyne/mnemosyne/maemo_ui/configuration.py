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

from mnemosyne.maemo_ui.widgets import create_configuration_ui
from mnemosyne.libmnemosyne.ui_components.dialogs import ConfigurationDialog

class ConfigurationWidget(ConfigurationDialog):
    """Configuration Widget."""

    def __init__(self, component_manager):
        ConfigurationDialog.__init__(self, component_manager)
        self.conf = self.config()
        self.current_size = self.conf['font_size']
        self.languages = []
        self.renderer = self.component_manager.get_current('renderer')
        # create widgets
        self.page, tts_settings_button, general_settings_button, \
            skin_settings_button, self.mode_settings_switcher, \
            self.checkbox_fullscreen_mode, self.checkbox_start_with_review, \
            self.imagedir_entry, self.sounddir_entry, self.tts_voice_label, \
            self.tts_pitch_label, self.tts_lang_label, self.tts_speed_label, \
            self.tts_speed_scrollbar, self.tts_pitch_scrollbar, self.font_size,\
            self.tts_lang_prev_button, tts_lang_next_button, menu_button, \
            font_size_decrease_button, font_size_increase_button, \
            tts_voice_prev_button, tts_voice_next_button = \
                create_configuration_ui(self.main_widget().switcher)
        # connect signals
        general_settings_button.connect('released', \
            self.show_general_settings_cb)
        skin_settings_button.connect('released', \
            self.show_skin_settings_cb)
        tts_settings_button.connect('released', self.show_tts_settings_cb)
        menu_button.connect('clicked', self.config_to_main_menu_cb)
        self.sounddir_entry.connect('changed', self.save_sounddir_value)
        self.imagedir_entry.connect('changed', self.save_imagedir_value)
        self.checkbox_fullscreen_mode.connect('toggled', \
            self.change_fullscreen_cb)
        self.checkbox_start_with_review.connect('toggled', \
            self.change_startup_with_review_cb)
        font_size_decrease_button.connect('clicked', self.change_font_size_cb)
        font_size_increase_button.connect('clicked', self.change_font_size_cb)
        self.tts_lang_prev_button.connect('clicked', self.change_lang_cb)
        tts_lang_next_button.connect('clicked', self.change_lang_cb)
        tts_voice_prev_button.connect('clicked', self.change_voice_cb)
        tts_voice_next_button.connect('clicked', self.change_voice_cb)
        self.tts_speed_scrollbar.connect('value-changed', self.change_speed_cb)
        self.tts_pitch_scrollbar.connect('value-changed', self.change_pitch_cb)
        
        page = self.conf['last_settings_page']
        tts_settings_button.set_sensitive(tts.is_available())
        if page == 0:
            general_settings_button.set_active(True)
            self.show_general_settings_cb(None)
        elif page == 1:
            skin_settings_button.set_active(True)
            self.show_skin_settings_cb(None)
        elif page == 2 and tts.is_available():
            tts_settings_button.set_active(True)
            self.show_tts_settings_cb(None)
        else:
            general_settings_button.set_active(True)
            tts_settings_button.set_sensitive(False)
            self.show_general_settings_cb(None)

    def activate(self):
        """Select necessary switcher page."""

        self.main_widget().switcher.set_current_page(self.page)

    def change_font_size(self):
        """Changes font size."""

        self.renderer.render_html(self.font_size, \
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

        self.mode_settings_switcher.set_current_page(0)
        self.checkbox_fullscreen_mode.set_active(self.conf['fullscreen'])
        self.checkbox_start_with_review.set_active( \
            self.conf['startup_with_review'])
        self.imagedir_entry.set_text(self.conf['imagedir'])
        self.sounddir_entry.set_text(self.conf['sounddir'])
        
    def show_tts_settings_cb(self, widget):
        """Switches to the tts settings page."""

        self.mode_settings_switcher.set_current_page(2)
        if not self.languages:
            self.languages = [lang for lang in tts.get_languages()]
        self.tts_voice_label.set_text(self.conf['tts_voice'])
        self.tts_lang_label.set_text(self.conf['tts_language'])
        self.tts_speed_scrollbar.set_value(self.conf['tts_speed'])
        self.tts_pitch_scrollbar.set_value(self.conf['tts_pitch'])
        self.change_speed_cb(self.tts_speed_scrollbar)
        self.change_pitch_cb(self.tts_pitch_scrollbar)

    def show_skin_settings_cb(self, widget):
        """Switches to the skin settings page."""

        self.mode_settings_switcher.set_current_page(1)
        self.change_font_size()

    def change_voice_cb(self, widget):
        """Changes TTS voice."""

        voices = {'Male': 'Female', 'Female': 'Male'}
        voice = self.tts_voice_label.get_text()
        new_voice = voices[voice]
        self.tts_voice_label.set_text(new_voice)
        self.conf['tts_voice'] = new_voice

    def change_lang_cb(self, widget):
        """Changes current TTS language."""

        lang_index = self.languages.index(self.tts_lang_label.get_text())
        direction = 1
        if widget == self.tts_lang_prev_button:
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
            self.tts_lang_label.set_text(new_lang)

    def change_speed_cb(self, widget):
        """Changes TTS speed."""

        value = int(widget.get_value())
        self.conf['tts_speed'] = value
        self.tts_speed_label.set_text("    Speed: %s" % value)

    def change_pitch_cb(self, widget):
        """Changes TTS pitch."""

        value = int(widget.get_value())
        self.conf['tts_pitch'] = value
        self.tts_pitch_label.set_text("    Pitch: %s" % value)

    def change_fullscreen_cb(self, widget):
        """Change Fullscreen parameter."""

        self.conf['fullscreen'] = \
            self.checkbox_fullscreen_mode.get_active()

    def change_startup_with_review_cb(self, widget):
        """Change 'Startup with Review' parameter."""

        self.conf['startup_with_review'] = \
            self.checkbox_start_with_review.get_active()

    def change_font_size_cb(self, widget):
        """Change Font size parameter."""

        min_size = 10
        max_size = 60
        if widget.name == "down_arrow":
            if self.current_size > min_size:
                self.current_size -= 1
        else:
            if self.current_size < max_size:
                self.current_size += 1
        self.change_font_size()
        self.conf['font_size'] = self.current_size

    def config_to_main_menu_cb(self, widget):
        """ Return to main menu. """

        if not os.path.exists(os.path.abspath(self.imagedir_entry.get_text())):
            self.main_widget().information_box(\
                _("Image directory does not exist! Select another."))
            return
        if not os.path.exists(os.path.abspath(self.sounddir_entry.get_text())):
            self.main_widget().information_box(\
                _("Sound directory does not exist! Select another."))
            return
        self.conf['last_settings_page'] = \
            self.mode_settings_switcher.get_current_page()
        self.conf.save()
        self.main_widget().switcher.remove_page(self.page)
        self.main_widget().menu_()


# Local Variables:
# mode: python
# py-indent-offset: 4
# indent-tabs-mode nil
# tab-width 4
# End:
