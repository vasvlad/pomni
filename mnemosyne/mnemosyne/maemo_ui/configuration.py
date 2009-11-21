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

        # create widgets
        toplevel_table = gtk.Table(rows=1, columns=2)
        toolbar_container = self.create_toolbar_container( \
            'config_mode_toolbar_container')
        toolbar_table = gtk.Table(rows=5, columns=1, homogeneous=True)
        general_settings_button = self.create_radio_button(None, \
            'config_toolbar_general_settings_button', \
            self.show_general_settings_cb, width=80, height=80)
        skin_settings_button = self.create_radio_button(general_settings_button, 
            'config_toolbar_skin_settings_button', \
            self.show_skin_settings_cb, width=80, height=80)
        tts_settings_button = self.create_radio_button(general_settings_button,
            'config_toolbar_tts_settings_button', self.show_tts_settings_cb, \
            width=80, height=80)
        menu_button = self.create_button('config_toolbar_main_menu_button', \
            self.config_to_main_menu_cb)
        mode_settings_switcher = gtk.Notebook()
        mode_settings_switcher.set_show_tabs(False)
        mode_settings_switcher.set_show_border(False)
        mode_settings_switcher.set_name('config_mode_settings_switcher')
        general_settings_table = gtk.Table(rows=2, columns=1, homogeneous=True)
        general_settings_table.set_row_spacings(10)
        directories_table = gtk.Table(rows=2, columns=1, homogeneous=True)
        directories_table.set_row_spacings(12)
        sounddir_box = gtk.VBox()
        sounddir_box.set_spacing(1)
        sounddir_label_container = gtk.HBox()
        sounddir_label = gtk.Label('  Sound directory:')
        sounddir_label.set_name('config_mode_label_sounddir')
        sounddir_container = gtk.Frame()
        sounddir_container.set_name('config_mode_sounddir_container')
        sounddir_entry = gtk.Entry()
        sounddir_entry.connect('changed', self.save_sounddir_value)
        sounddir_entry.set_name('config_mode_entry_sounddir')
        imagedir_box = gtk.VBox()
        imagedir_box.set_spacing(1)
        imagedir_label_container = gtk.HBox()
        imagedir_label = gtk.Label('  Image directory:')
        imagedir_label.set_name('config_mode_label_imagedir')
        imagedir_container = gtk.Frame()
        imagedir_container.set_name('config_mode_imagedir_container')
        imagedir_entry = gtk.Entry()
        imagedir_entry.connect('changed', self.save_imagedir_value)
        imagedir_entry.set_name('config_mode_entry_imagedir')
        checkboxes_box = gtk.VBox(homogeneous=True)
        checkboxes_box.set_spacing(12)
        fullscreen_table = gtk.Table(rows=1, columns=2)
        fullscreen_table.set_col_spacings(10)
        fullscreen_checkbox = gtk.ToggleButton()
        fullscreen_checkbox.connect('toggled', self.change_fullscreen_cb)
        fullscreen_checkbox.set_size_request(64, 64)
        fullscreen_checkbox.set_name('checkbox_fullscreen_mode')
        fullscreen_label = gtk.Label('Start in Fullscreen mode')
        fullscreen_label.set_name('config_mode_fullscreen_label')
        start_with_review_table = gtk.Table(rows=1, columns=2)
        start_with_review_table.set_col_spacings(10)
        start_with_review_checkbox = gtk.ToggleButton()
        start_with_review_checkbox.connect('toggled', \
            self.change_startup_with_review_cb)
        start_with_review_checkbox.set_size_request(64, 64)
        start_with_review_checkbox.set_name('checkbox_start_in_review_mode')
        start_with_review_label = gtk.Label('Open Review mode at startup')
        start_with_review_label.set_name('config_mode_startup_with_review_label')
        skin_settings_table = gtk.Table(rows=1, columns=1)
        font_size_table = gtk.Table(rows=1, columns=3)
        font_size_example_container = gtk.Frame()
        font_size_example_container.set_size_request(-1, 140)
        font_size_example_container.set_name( \
            'config_mode_font_size_example_container')
        font_size = self.main_widget().create_gtkhtml()
        font_size_decrease_button = self.create_button(
            'config_mode_decrease_font_size_buttton', self.change_font_size_cb,
            width=64, height=64)
        font_size_increase_button = self.create_button( \
            'config_mode_increase_font_size_buttton', self.change_font_size_cb,
            width=64, height=64)
        tts_settings_table = gtk.Table(rows=2, columns=1, homogeneous=True)
        tts_settings_table1 = gtk.Table(rows=2, columns=1, homogeneous=True)
        tts_settings_table1.set_row_spacings(10)
        tts_lang_table = gtk.Table(rows=1, columns=3)
        tts_lang_container = self.create_button( \
            'config_mode_tts_lang_container', width=-1, height=60)
        tts_lang_label = gtk.Label('default')
        tts_lang_label.set_name('config_mode_tts_lang_label')
        tts_lang_prev_button = self.create_button( \
            'config_mode_tts_lang_prev_button', self.change_lang_cb)
        tts_lang_next_button = self.create_button( \
            'config_mode_tts_lang_next_button', self.change_lang_cb)
        tts_voice_table = gtk.Table(rows=1, columns=3)
        tts_voice_container = self.create_button( \
            'config_mode_tts_voice_container', width=-1, height=60)
        tts_voice_label = gtk.Label('Male')
        tts_voice_label.set_name('config_mode_tts_voice_label')
        tts_voice_prev_button = self.create_button( \
            'config_mode_tts_voice_prev_button', self.change_voice_cb)
        tts_voice_next_button = self.create_button( \
            'config_mode_tts_voice_next_button', self.change_voice_cb)
        tts_settings_table2 = gtk.Table(rows=2, columns=1, homogeneous=True)
        tts_settings_table2.set_row_spacings(10)
        tts_speed_box = gtk.VBox()
        tts_speed_box.set_spacing(10)
        tts_speed_label_box = gtk.HBox()
        tts_speed_label = gtk.Label('Speed:')
        tts_speed_label.set_name('config_mode_tts_speed_label')
        tts_speed_scrollbar = gtk.HScrollbar()
        tts_speed_scrollbar.set_adjustment(gtk.Adjustment(lower=30, upper=200))
        tts_speed_scrollbar.set_increments(step=1, page=10)
        tts_speed_scrollbar.set_update_policy(gtk.UPDATE_CONTINUOUS)
        tts_speed_scrollbar.connect('value-changed', self.change_speed_cb)
        tts_speed_scrollbar.set_name('config_mode_tts_speed_scrollbar')
        tts_pitch_box = gtk.VBox()
        tts_pitch_box.set_spacing(10)
        tts_pitch_label_box = gtk.HBox()
        tts_pitch_label = gtk.Label('Pitch:')
        tts_pitch_label.set_name('config_mode_tts_pitch_label')
        tts_pitch_scrollbar = gtk.HScrollbar()
        tts_pitch_scrollbar.set_update_policy(gtk.UPDATE_CONTINUOUS)
        tts_pitch_scrollbar.set_adjustment(gtk.Adjustment(lower=0, upper=100))
        tts_pitch_scrollbar.set_increments(step=1, page=10)
        tts_pitch_scrollbar.connect('value-changed', self.change_pitch_cb)
        tts_pitch_scrollbar.set_name('config_mode_tts_pitch_scrollbar')
        # packing widgets
        toolbar_table.attach(general_settings_button, 0, 1, 0, 1, \
            xoptions=gtk.SHRINK, yoptions=gtk.EXPAND)
        toolbar_table.attach(skin_settings_button, 0, 1, 1, 2, \
            xoptions=gtk.SHRINK, yoptions=gtk.EXPAND)
        toolbar_table.attach(tts_settings_button, 0, 1, 2, 3, \
            xoptions=gtk.SHRINK, yoptions=gtk.EXPAND)
        toolbar_table.attach(menu_button, 0, 1, 4, 5, \
            xoptions=gtk.SHRINK, yoptions=gtk.EXPAND)
        toolbar_container.add(toolbar_table)
        toplevel_table.attach(toolbar_container, 0, 1, 0, 1, \
            xoptions=gtk.SHRINK, yoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL)
        imagedir_container.add(imagedir_entry)
        imagedir_label_container.pack_start(imagedir_label, expand=False, \
            fill=False)
        imagedir_box.pack_start(imagedir_label_container)
        imagedir_box.pack_end(imagedir_container)
        sounddir_container.add(sounddir_entry)
        sounddir_label_container.pack_start(sounddir_label, expand=False, \
            fill=False)
        sounddir_box.pack_start(sounddir_label_container)
        sounddir_box.pack_end(sounddir_container)
        directories_table.attach(sounddir_box, 0, 1, 0, 1, xpadding=14, \
            xoptions=gtk.EXPAND|gtk.FILL|gtk.SHRINK, \
            yoptions=gtk.EXPAND|gtk.SHRINK)
        directories_table.attach(imagedir_box, 0, 1, 1, 2, xpadding=14, \
            xoptions=gtk.EXPAND|gtk.FILL|gtk.SHRINK, \
            yoptions=gtk.EXPAND|gtk.SHRINK)
        start_with_review_table.attach(start_with_review_checkbox, 0, 1, 0, 1, \
            xoptions=gtk.SHRINK, yoptions=gtk.EXPAND|gtk.FILL)
        start_with_review_table.attach(start_with_review_label, 1, 2, 0, 1, \
            xoptions=gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL)
        fullscreen_table.attach(fullscreen_checkbox, 0, 1, 0, 1, \
            xoptions=gtk.SHRINK, yoptions=gtk.EXPAND|gtk.SHRINK)
        fullscreen_table.attach(fullscreen_label, 1, 2, 0, 1, \
            xoptions=gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL)
        checkboxes_box.pack_start(fullscreen_table)
        checkboxes_box.pack_end(start_with_review_table)
        general_settings_table.attach(directories_table, 0, 1, 0, 1, \
            xoptions=gtk.EXPAND|gtk.FILL|gtk.SHRINK, ypadding=10, 
            yoptions=gtk.EXPAND|gtk.FILL|gtk.SHRINK)
        general_settings_table.attach(checkboxes_box, 0, 1, 1, 2, \
            xoptions=gtk.EXPAND|gtk.FILL|gtk.SHRINK, xpadding=13, \
            yoptions=gtk.EXPAND|gtk.SHRINK)
        mode_settings_switcher.append_page(general_settings_table)

        font_size_example_container.add(font_size)
        font_size_table.attach(font_size_decrease_button, 0, 1, 0, 1, \
            xoptions=gtk.SHRINK, yoptions=gtk.EXPAND)
        font_size_table.attach(font_size_example_container, 1, 2, 0, 1, \
            xoptions=gtk.EXPAND|gtk.FILL, xpadding=14, \
            yoptions=gtk.EXPAND|gtk.FILL|gtk.SHRINK)
        font_size_table.attach(font_size_increase_button, 2, 3, 0, 1, \
            xoptions=gtk.SHRINK, yoptions=gtk.EXPAND)
        skin_settings_table.attach(font_size_table, 0, 1, 0, 1, \
            xoptions=gtk.EXPAND|gtk.FILL|gtk.SHRINK, yoptions=gtk.EXPAND)
        mode_settings_switcher.append_page(skin_settings_table)

        tts_voice_container.add(tts_voice_label)
        tts_voice_table.attach(tts_voice_prev_button, 0, 1, 0, 1, \
            xoptions=gtk.SHRINK, yoptions=gtk.EXPAND)
        tts_voice_table.attach(tts_voice_container, 1, 2, 0, 1, \
            xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.SHRINK)
        tts_voice_table.attach(tts_voice_next_button, 2, 3, 0, 1, \
            xoptions=gtk.SHRINK, yoptions=gtk.EXPAND)
        tts_lang_container.add(tts_lang_label)
        tts_lang_table.attach(tts_lang_prev_button, 0, 1, 0, 1, \
            xoptions=gtk.SHRINK, yoptions=gtk.EXPAND)
        tts_lang_table.attach(tts_lang_container, 1, 2, 0, 1, \
            xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.SHRINK)
        tts_lang_table.attach(tts_lang_next_button, 2, 3, 0, 1, \
            xoptions=gtk.SHRINK, yoptions=gtk.EXPAND)
        tts_speed_label_box.pack_start(tts_speed_label, expand=False, fill=False)
        tts_speed_box.pack_start(tts_speed_label_box, expand=False, fill=False)
        tts_speed_box.pack_end(tts_speed_scrollbar)
        tts_pitch_label_box.pack_start(tts_pitch_label, expand=False, fill=False)
        tts_pitch_box.pack_start(tts_pitch_label_box, expand=False, fill=False)
        tts_pitch_box.pack_end(tts_pitch_scrollbar)
        tts_settings_table2.attach(tts_speed_box, 0, 1, 0, 1, \
            xoptions=gtk.EXPAND|gtk.FILL|gtk.SHRINK, \
            yoptions=gtk.EXPAND|gtk.FILL|gtk.SHRINK)
        tts_settings_table2.attach(tts_pitch_box, 0, 1, 1, 2, \
            xoptions=gtk.EXPAND|gtk.FILL|gtk.SHRINK, \
            yoptions=gtk.EXPAND|gtk.FILL|gtk.SHRINK)
        tts_settings_table1.attach(tts_lang_table, 0, 1, 0, 1, \
            xoptions=gtk.EXPAND|gtk.FILL|gtk.SHRINK, \
            yoptions=gtk.EXPAND|gtk.FILL|gtk.SHRINK)
        tts_settings_table1.attach(tts_voice_table, 0, 1, 1, 2, \
            xoptions=gtk.EXPAND|gtk.FILL|gtk.SHRINK, \
            yoptions=gtk.EXPAND|gtk.FILL|gtk.SHRINK)
        tts_settings_table.attach(tts_settings_table1, 0, 1, 0, 1, \
            xoptions=gtk.EXPAND|gtk.FILL|gtk.SHRINK, \
            yoptions=gtk.EXPAND|gtk.FILL|gtk.SHRINK)
        tts_settings_table.attach(tts_settings_table2, 0, 1, 1, 2, \
            xoptions=gtk.EXPAND|gtk.FILL|gtk.SHRINK, \
            yoptions=gtk.EXPAND|gtk.FILL|gtk.SHRINK)
        mode_settings_switcher.append_page(tts_settings_table)
        toplevel_table.attach(mode_settings_switcher, 1, 2, 0, 1, \
            xoptions=gtk.EXPAND|gtk.FILL|gtk.SHRINK, xpadding = 14, \
            yoptions=gtk.EXPAND|gtk.FILL|gtk.SHRINK, ypadding=14)
        toplevel_table.show_all()
        self.page = self.main_widget().switcher.append_page(toplevel_table)
        # create attributes
        self.tts_settings_button = tts_settings_button
        self.general_settings_button = general_settings_button
        self.skin_settings_button = skin_settings_button
        self.mode_settings_switcher = mode_settings_switcher
        self.checkbox_fullscreen_mode = fullscreen_checkbox
        self.checkbox_start_with_review = start_with_review_checkbox
        self.imagedir_entry = imagedir_entry
        self.sounddir_entry = sounddir_entry
        self.tts_voice_label = tts_voice_label
        self.tts_pitch_label = tts_pitch_label
        self.tts_lang_label = tts_lang_label
        self.tts_speed_label = tts_speed_label
        self.tts_speed_scrollbar = tts_speed_scrollbar
        self.tts_pitch_scrollbar = tts_pitch_scrollbar
        self.font_size = font_size
        self.tts_lang_prev_button = tts_lang_prev_button
        self.tts_lang_next_button = tts_lang_next_button

        page = self.conf['last_settings_page']
        self.tts_settings_button.set_sensitive(tts.is_available())
        if page == 0:
            self.general_settings_button.set_active(True)
            self.show_general_settings_cb(None)
        elif page == 1:
            self.skin_settings_button.set_active(True)
            self.show_skin_settings_cb(None)
        elif page == 2 and tts.is_available():
            self.tts_settings_button.set_active(True)
            self.show_tts_settings_cb(None)
        else:
            self.general_settings_button.set_active(True)
            self.tts_settings_button.set_sensitive(False)
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
