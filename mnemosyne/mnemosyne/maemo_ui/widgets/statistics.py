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
Hildon UI. Statistics widget.
"""

import gtk
import mnemosyne.maemo_ui.widgets.common as widgets

def create_statistics_ui(main_switcher, current_card_text, common_text):
    """Creates MaemoStatisticsWidget UI."""
    def create_toolbar_container(name, show_tabs=False, width=82, height=480):
        """Creates toolbar container."""

        container = gtk.Notebook()
        container.set_show_tabs(show_tabs)
        container.set_size_request(width, height)
        container.set_name(name)
        return container

    toplevel_table = gtk.Table(rows=1, columns=2)
    toolbar_container = create_toolbar_container('toolbar_container')
    toolbar_table = gtk.Table(rows=5, columns=1, homogeneous=True)
    current_card_button = widgets.create_radio_button(None, \
        'stat_toolbar_current_card_button', None, width=80, height=80)
    common_button = widgets.create_radio_button(current_card_button, \
        'stat_toolbar_common_stat_button', None, width=80, height=80)
    tags_button = widgets.create_radio_button(common_button, \
        'stat_toolbar_tags_stat_button', None, width=80, height=80)


    menu_button = widgets.create_button('main_menu_button', None)


# packing toolbar buttons
    # packing widgets
    toolbar_table.attach(current_card_button,  0, 1, 0, 1, \
        xoptions=gtk.SHRINK, yoptions=gtk.EXPAND)
    toolbar_table.attach(common_button, 0, 1, 1, 2, \
        xoptions=gtk.SHRINK, yoptions=gtk.EXPAND)
    toolbar_table.attach(tags_button, 0, 1, 2, 3, \
        xoptions=gtk.SHRINK, yoptions=gtk.EXPAND)
    toolbar_table.attach(menu_button, 0, 1, 4, 5, \
        xoptions=gtk.SHRINK, yoptions=gtk.EXPAND)
    toolbar_container.add(toolbar_table)
    toplevel_table.attach(toolbar_container, 0, 1, 0, 1, \
        xoptions=gtk.SHRINK, yoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL)

    mode_statistics_switcher = gtk.Notebook()
    mode_statistics_switcher.set_show_tabs(False)
    mode_statistics_switcher.set_show_border(False)
    mode_statistics_switcher.set_name('config_mode_settings_switcher')

    current_card_box = gtk.VBox()
    label_title = gtk.Label()
    label_title.set_use_markup(True)
    label_title.set_justify(gtk.JUSTIFY_CENTER)
    label_title.set_markup("<span foreground='white' size='x-large'><b>"\
        "Current card statistics</b></span>")
    label_text = gtk.Label()
    label_text.set_use_markup(True)
    label_text.set_justify(gtk.JUSTIFY_LEFT)
    label_text.set_markup(current_card_text)
    current_card_box.pack_start(label_title, expand=False, fill=True, padding=10)
    current_card_box.pack_start(label_text, expand=False, fill=True, padding=10)
    mode_statistics_switcher.append_page(current_card_box)
  
    common_box = gtk.VBox()
    label_title = gtk.Label()
    label_title.set_use_markup(True)
    label_title.set_justify(gtk.JUSTIFY_CENTER)
    label_title.set_markup("<span foreground='white' size='x-large'><b>"\
        "Grade statistics for all cards</b></span>")
    label_text = gtk.Label()
    label_text.set_use_markup(True)
    label_text.set_justify(gtk.JUSTIFY_LEFT)
    label_text.set_markup(common_text)
    common_box.pack_start(label_title, expand=False, fill=True, padding=10)
    common_box.pack_start(label_text, expand=False, fill=True, padding=10)
    mode_statistics_switcher.append_page(common_box)
  
    toplevel_table.attach(mode_statistics_switcher, 1, 2, 0, 1, \
        xoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL, \
        yoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL)
    toplevel_table.show_all()
    return main_switcher.append_page(toplevel_table), mode_statistics_switcher, \
           menu_button, current_card_button, common_button, tags_button 


