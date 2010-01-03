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
Hildon UI. Widgets for main.
"""

import gtk
from mnemosyne.maemo_ui.widgets.common import create_tag_checkbox

import mnemosyne.maemo_ui.widgets.common as widgets

def create_tags_ui(main_switcher):
    """Creates TagsWidget UI."""

    def create_button(name, width=80, height=80):
        button = gtk.Button()
        button.set_size_request(width, height)
        button.set_name(name)
        return button

    toplevel_table = gtk.Table(rows=1, columns=2, homogeneous=False)
    # create toolbar container
    toolbar_container = gtk.Notebook()
    toolbar_container.set_show_tabs(False)
    toolbar_container.set_size_request(82, 480)
    toolbar_container.set_name('review_toolbar_container')
 
    toolbar_table = gtk.Table(rows=5, columns=1, homogeneous=True)
    
    # create toolbar buttons
    buttons = {}
    buttons[4] = create_button('stat_button')
    buttons[5] = create_button('main_menu_button')
 

    # packing toolbar buttons
    for pos in buttons.keys():
        toolbar_table.attach(buttons[pos], 0, 1, pos, pos + 1, \
            xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
    toolbar_container.add(toolbar_table)
 
    # create tags frame
    tags_frame = gtk.Frame()
    tags_frame.set_name('html_container')
    tags_eventbox = gtk.EventBox()
    tags_eventbox.set_visible_window(True)
    tags_eventbox.set_name('viewport_widget')
    tags_scrolledwindow = gtk.ScrolledWindow()
    tags_scrolledwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    tags_scrolledwindow.set_name('scrolled_window')
    tags_viewport = gtk.Viewport()
    tags_viewport.set_shadow_type(gtk.SHADOW_NONE)
    tags_viewport.set_name('viewport_widget')
    tags_box = gtk.VBox()
    # packing widgets
    tags_viewport.add(tags_box)
    tags_scrolledwindow.add(tags_viewport)
    tags_eventbox.add(tags_scrolledwindow)
    tags_frame.add(tags_eventbox)
    toplevel_table.attach(toolbar_container, 0, 1, 0, 1, \
       xoptions=gtk.SHRINK, yoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL)
    toplevel_table.attach(tags_frame, 1, 2, 0, 1, \
        xoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL, \
        yoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL, \
        xpadding=30, ypadding=30)
    toplevel_table.show_all()
    return main_switcher.append_page(toplevel_table), tags_box, buttons[5], \
           buttons[4]

