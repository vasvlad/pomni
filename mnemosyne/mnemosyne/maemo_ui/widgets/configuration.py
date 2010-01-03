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
Hildon UI. Widgets for configuration mode.
"""

import gtk
import mnemosyne.maemo_ui.widgets.common as widgets

def create_configuration_ui(main_switcher):
    """Creates ConfigureWidget UI."""

    def create_toolbar_container(name, show_tabs=False, width=82, height=480):
        """Creates toolbar container."""

        container = gtk.Notebook()
        container.set_show_tabs(show_tabs)
        container.set_size_request(width, height)
        container.set_name(name)
        return container

    toplevel_table = gtk.Table(rows=1, columns=2)
    toolbar_container = create_toolbar_container('input_toolbar_container')
    toolbar_table = gtk.Table(rows=5, columns=1, homogeneous=True)
    general_settings_button = widgets.create_radio_button(None, \
        'config_toolbar_general_settings_button', None, width=80, height=80)
    skin_settings_button = widgets.create_radio_button(general_settings_button,
        'config_toolbar_skin_settings_button', None, width=80, height=80)
    tts_settings_button = widgets.create_radio_button(general_settings_button,
        'config_toolbar_tts_settings_button', None, width=80, height=80)
    menu_button = widgets.create_button('main_menu_button', None)
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
    sounddir_label.set_name('white_label')
    sounddir_container = gtk.Frame()
    sounddir_container.set_name('html_container')
    sounddir_entry = gtk.Entry()
    sounddir_entry.set_name('entry_widget')
    imagedir_box = gtk.VBox()
    imagedir_box.set_spacing(1)
    imagedir_label_container = gtk.HBox()
    imagedir_label = gtk.Label('  Image directory:')
    imagedir_label.set_name('white_label')
    imagedir_container = gtk.Frame()
    imagedir_container.set_name('html_container')
    imagedir_entry = gtk.Entry()
    imagedir_entry.set_name('entry_widget')
    checkboxes_box = gtk.VBox(homogeneous=True)
    checkboxes_box.set_spacing(12)
    fullscreen_table = gtk.Table(rows=1, columns=2)
    fullscreen_table.set_col_spacings(10)
    fullscreen_checkbox = gtk.ToggleButton()
    fullscreen_checkbox.set_size_request(64, 64)
    fullscreen_checkbox.set_name('config_checkbox')
    fullscreen_label = gtk.Label('Start in Fullscreen mode')
    fullscreen_label.set_name('white_label')
    start_with_review_table = gtk.Table(rows=1, columns=2)
    start_with_review_table.set_col_spacings(10)
    start_with_review_checkbox = gtk.ToggleButton()
    start_with_review_checkbox.set_size_request(64, 64)
    start_with_review_checkbox.set_name('config_checkbox')
    start_with_review_label = gtk.Label('Open Review mode at startup')
    start_with_review_label.set_name('white_label')
    skin_settings_table = gtk.Table(rows=1, columns=1)
    font_size_table = gtk.Table(rows=1, columns=3)
    font_size_example_container = gtk.Frame()
    font_size_example_container.set_size_request(-1, 140)
    font_size_example_container.set_name('html_container')
    font_size = widgets.create_gtkhtml()
    font_size_decrease_button = widgets.create_button('down_arrow', None,
        width=64, height=64)
    font_size_increase_button = widgets.create_button('up_arrow', None, 
        width=64, height=64)
    tts_settings_table = gtk.Table(rows=2, columns=1, homogeneous=True)
    tts_settings_table1 = gtk.Table(rows=2, columns=1, homogeneous=True)
    tts_settings_table1.set_row_spacings(10)
    tts_lang_table = gtk.Table(rows=1, columns=3)
    tts_lang_container = widgets.create_button('labels_container', 
        width=-1, height=60)
    tts_lang_label = gtk.Label('default')
    tts_lang_label.set_name('config_tts_label')
    tts_lang_prev_button = widgets.create_button('main_menu_button', None)
    tts_lang_next_button = widgets.create_button('right_arrow', None)
    tts_voice_table = gtk.Table(rows=1, columns=3)
    tts_voice_container = widgets.create_button('labels_container', 
        width=-1, height=60)
    tts_voice_label = gtk.Label('Male')
    tts_voice_label.set_name('config_tts_label')
    tts_voice_prev_button = widgets.create_button('main_menu_button', \
        None)
    tts_voice_next_button = widgets.create_button('right_arrow', None)
    tts_settings_table2 = gtk.Table(rows=2, columns=1, homogeneous=True)
    tts_settings_table2.set_row_spacings(10)
    tts_speed_box = gtk.VBox()
    tts_speed_box.set_spacing(10)
    tts_speed_label_box = gtk.HBox()
    tts_speed_label = gtk.Label('Speed:')
    tts_speed_label.set_name('config_scrollbar_label')
    tts_speed_scrollbar = gtk.HScrollbar()
    tts_speed_scrollbar.set_adjustment(gtk.Adjustment(lower=30, upper=200))
    tts_speed_scrollbar.set_increments(step=1, page=10)
    tts_speed_scrollbar.set_update_policy(gtk.UPDATE_CONTINUOUS)
    tts_speed_scrollbar.set_name('config_scrollbar')
    tts_pitch_box = gtk.VBox()
    tts_pitch_box.set_spacing(10)
    tts_pitch_label_box = gtk.HBox()
    tts_pitch_label = gtk.Label('Pitch:')
    tts_pitch_label.set_name('config_scrollbar_label')
    tts_pitch_scrollbar = gtk.HScrollbar()
    tts_pitch_scrollbar.set_update_policy(gtk.UPDATE_CONTINUOUS)
    tts_pitch_scrollbar.set_adjustment(gtk.Adjustment(lower=0, upper=100))
    tts_pitch_scrollbar.set_increments(step=1, page=10)
    tts_pitch_scrollbar.set_name('config_scrollbar')
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
    imagedir_label_container.pack_start(imagedir_label, expand=False, 
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
    return main_switcher.append_page(toplevel_table), tts_settings_button, \
        general_settings_button, skin_settings_button, mode_settings_switcher,\
        fullscreen_checkbox, start_with_review_checkbox, imagedir_entry, \
        sounddir_entry, tts_voice_label, tts_pitch_label, tts_lang_label, \
        tts_speed_label, tts_speed_scrollbar, tts_pitch_scrollbar, font_size, \
        tts_lang_prev_button, tts_lang_next_button, menu_button, \
        font_size_decrease_button, font_size_increase_button, \
        tts_voice_prev_button, tts_voice_next_button



