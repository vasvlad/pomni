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

def create_statistics_ui(main_switcher):
    """Creates MaemoStatisticsWidget UI."""

    toplevel_table = gtk.Table(rows=1, columns=2)
    toolbar_container = widgets.create_toolbar_container('toolbar_container')
    toolbar_table = gtk.Table(rows=5, columns=1, homogeneous=True)
    # create toolbar buttons
    current_card_button = widgets.create_radio_button(None, \
        'stat_toolbar_current_card_button', None, width=80, height=80)
    common_button = widgets.create_radio_button(current_card_button, \
        'stat_toolbar_common_stat_button', None, width=80, height=80)
    tags_button = widgets.create_radio_button(common_button, \
        'stat_toolbar_tags_stat_button', None, width=80, height=80)
    menu_button = widgets.create_button('main_menu_button', None)
    # create mode switcher
    mode_statistics_switcher = gtk.Notebook()
    mode_statistics_switcher.set_show_tabs(False)
    mode_statistics_switcher.set_show_border(False)
    mode_statistics_switcher.set_name('config_mode_settings_switcher')
    # packing toolbar buttons
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
    # create widgets for current card mode
    current_card_table = gtk.Table(rows=1, columns=1, homogeneous=False)
    current_card_frame = gtk.Frame()
    current_card_frame.set_name('html_container')
    current_card_eventbox = gtk.EventBox()
    current_card_eventbox.set_visible_window(True)
    current_card_eventbox.set_name('viewport_widget')
    current_card_scrolledwindow = gtk.ScrolledWindow()
    current_card_scrolledwindow.set_policy(gtk.POLICY_AUTOMATIC, \
        gtk.POLICY_AUTOMATIC)
    current_card_scrolledwindow.set_name('scrolled_window')
    current_card_html = widgets.create_gtkhtml()
    # packing widgets for current card mode
    current_card_table.attach(current_card_frame, 1, 2, 0, 1, \
        xoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL, \
        yoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL, \
        xpadding=30, ypadding=30)
    current_card_scrolledwindow.add(current_card_html)
    current_card_eventbox.add(current_card_scrolledwindow)
    current_card_frame.add(current_card_eventbox)
    mode_statistics_switcher.append_page(current_card_table)
    # create widgets for total cards mode
    total_card_table = gtk.Table(rows=1, columns=1, homogeneous=False)
    total_card_frame = gtk.Frame()
    total_card_frame.set_name('html_container')
    total_card_eventbox = gtk.EventBox()
    total_card_eventbox.set_visible_window(True)
    total_card_eventbox.set_name('viewport_widget')
    total_card_scrolledwindow = gtk.ScrolledWindow()
    total_card_scrolledwindow.set_policy(gtk.POLICY_AUTOMATIC, \
        gtk.POLICY_AUTOMATIC)
    total_card_scrolledwindow.set_name('scrolled_window')
    total_card_html = widgets.create_gtkhtml()
    # packing widgets for total cards mode
    total_card_table.attach(total_card_frame, 1, 2, 0, 1, \
        xoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL, \
        yoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL, \
        xpadding=30, ypadding=30)
    total_card_scrolledwindow.add(total_card_html)
    total_card_eventbox.add(total_card_scrolledwindow)
    total_card_frame.add(total_card_eventbox)
    mode_statistics_switcher.append_page(total_card_table)
    # create widgets for grades section
    tags_card_table = gtk.Table(rows=1, columns=1, homogeneous=False)
    tags_card_frame = gtk.Frame()
    tags_card_frame.set_name('html_container')
    tags_card_eventbox = gtk.EventBox()
    tags_card_eventbox.set_visible_window(True)
    tags_card_eventbox.set_name('viewport_widget')
    tags_card_scrolledwindow = gtk.ScrolledWindow()
    tags_card_scrolledwindow.set_policy(gtk.POLICY_AUTOMATIC, \
        gtk.POLICY_AUTOMATIC)
    tags_card_scrolledwindow.set_name('scrolled_window')
    tags_card_html = widgets.create_gtkhtml()
    # packing widgets for grades section
    tags_card_table.attach(tags_card_frame, 1, 2, 0, 1, \
        xoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL, \
        yoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL, \
        xpadding=30, ypadding=30)
    tags_card_scrolledwindow.add(tags_card_html)
    tags_card_eventbox.add(tags_card_scrolledwindow)
    tags_card_frame.add(tags_card_eventbox)
    mode_statistics_switcher.append_page(tags_card_table)
    # packing widgets
    toplevel_table.attach(mode_statistics_switcher, 1, 2, 0, 1, \
        xoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL, \
        yoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL)
    toplevel_table.show_all()
    return main_switcher.append_page(toplevel_table), \
        mode_statistics_switcher, menu_button, current_card_button, \
        common_button, tags_button, current_card_html, total_card_html, \
        tags_card_html
