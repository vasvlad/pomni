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
Hildon UI. Import widget.
"""

import gtk
import mnemosyne.maemo_ui.widgets.common as widgets

def create_importcard_ui(main_switcher):
    """Creates MaemoImportWidget UI."""

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
    # create toolbar buttons
    menu_button = widgets.create_button('main_menu_button', None)
    notebook = gtk.Notebook()
    notebook.set_show_tabs(False)
    notebook.set_show_border(False)
    notebook.set_name('config_mode_settings_switcher')

    #Create main table 
    general_settings_table = gtk.Table(rows=2, columns=1, homogeneous=True)
    general_settings_table.set_row_spacings(10)

    #Create format selector 
    format_table = gtk.Table(rows=2, columns=1, homogeneous=True)
    format_table = gtk.Table(rows=2, columns=1, homogeneous=True)
    format_table.set_row_spacings(10)
    #Button of selected format
    format_container = widgets.create_button('labels_container', 
        width=-1, height=60)
    format_label = gtk.Label('default')
    format_label.set_name('format_label')
    format_prev_button = widgets.create_button('left_arrow', None)
    format_next_button = widgets.create_button('right_arrow', None)
    # Package of selected widgets
    format_container.add(format_label)
    format_table.attach(tts_voice_prev_button, 0, 1, 0, 1, \
        xoptions=gtk.SHRINK, yoptions=gtk.EXPAND)
    format_table.attach(tts_voice_container, 1, 2, 0, 1, \
        xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.SHRINK)
    format_table.attach(tts_voice_next_button, 2, 3, 0, 1, \
        xoptions=gtk.SHRINK, yoptions=gtk.EXPAND)

    # create OK button
    ok_button = widgets.create_button('ok_button', None)
    # packing toolbar buttons
    toolbar_table.attach(menu_button, 0, 1, 4, 5, \
        xoptions=gtk.SHRINK, yoptions=gtk.EXPAND)
    toolbar_container.add(toolbar_table)
    toplevel_table.attach(toolbar_container, 0, 1, 0, 1, \
        xoptions=gtk.SHRINK, yoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL)
    # packing widgets
    notebook.add(ok_button) 
    notebook.add(format_table) 
    toplevel_table.attach(notebook, 1, 2, 0, 1, \
        xoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL, \
        yoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL)

    toplevel_table.show_all()

    return main_switcher.append_page(toplevel_table), \
           menu_button, ok_button

