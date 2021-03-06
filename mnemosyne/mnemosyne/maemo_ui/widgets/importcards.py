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

def choose_file_cb(self, file_name_label, ok_button, main_window) :
        try:
            import hildon
            dlg = hildon.FileChooserDialog(main_window, gtk.FILE_CHOOSER_ACTION_OPEN);
        except ImportError:
            dlg = gtk.FileChooserDialog( title="Choose File.", parent = None, action = gtk.FILE_CHOOSER_ACTION_OPEN)
            dlg.add_button( gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
            dlg.add_button( gtk.STOCK_SAVE, gtk.RESPONSE_OK)
        response = dlg.run() 
        if response == gtk.RESPONSE_OK:
            file_name_label.set_text(dlg.get_filename())
            file_name_label.set_line_wrap(True)
            file_name_label.show()
            dlg.destroy()
            ok_button.set_sensitive(True)
        else:
            dlg.destroy()

def create_importcard_ui(main_window, main_switcher, format_desc):
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

    #Create main table 
    general_settings_table = gtk.Table(rows=4, columns=1, homogeneous=False)
    general_settings_table.set_row_spacings(10)

    #Create format selector 
    format_table = gtk.Table(rows=1, columns=3, homogeneous=False)
    #Button of selected format
    format_container = widgets.create_button('labels_container', 
        width=-1, height=60)
    format_label = gtk.Label(format_desc)
    format_label.set_name('config_import_label')
    format_prev_button = widgets.create_button('left_arrow', None)
    format_next_button = widgets.create_button('right_arrow', None)
    # Package of selected widgets
    format_container.add(format_label)
    format_table.attach(format_prev_button, 0, 1, 0, 1, \
       xoptions=gtk.SHRINK, yoptions=gtk.EXPAND)
    format_table.attach(format_container, 1, 2, 0, 1, \
        xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.SHRINK)
    format_table.attach(format_next_button, 2, 3, 0, 1, \
        xoptions=gtk.SHRINK, yoptions=gtk.SHRINK)
    
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

    # create filename button
    file_name_button = widgets.create_button('labels_container', None)
    file_name_label = gtk.Label('Press here for choosing file')
    file_name_label.set_name('config_import_label')
    file_name_label.set_alignment(0.5, 0.5)
    file_name_button.add(file_name_label)

    # create OK button
    ok_button = widgets.create_button('labels_container', None)
    ok_label = gtk.Label('Go!')
    ok_label.set_name('config_import_label')
    ok_button.set_sensitive(False)
    ok_button.add(ok_label)

    file_name_button.connect('clicked', choose_file_cb, file_name_label, ok_button, main_window)

    #packing widget to table
    general_settings_table.attach(format_table, 0, 1, 0, 1, \
        xoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL, \
        yoptions=gtk.SHRINK)

    general_settings_table.attach(tags_frame, 0, 1, 1, 2, \
       xoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL, \
       yoptions=gtk.SHRINK|gtk.FILL, \
       xpadding=30, ypadding=10)

    general_settings_table.attach(file_name_button, 0, 1, 2, 3, \
        xoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL, \
        yoptions=gtk.SHRINK)
      
    general_settings_table.attach(ok_button, 0, 1, 3, 4, \
        xoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL, \
        yoptions=gtk.SHRINK)

    # packing toolbar buttons
    toolbar_table.attach(menu_button, 0, 1, 4, 5, \
        xoptions=gtk.SHRINK, yoptions=gtk.EXPAND)
    toolbar_container.add(toolbar_table)

    # packing widgets in toplevel table
    toplevel_table.attach(toolbar_container, 0, 1, 0, 1, \
        xoptions=gtk.SHRINK, yoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL)

    toplevel_table.attach(general_settings_table, 1, 2, 0, 1, \
        xoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL, \
        yoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL)

    toplevel_table.show_all()

    return main_switcher.append_page(toplevel_table), format_label, \
           tags_box, menu_button, ok_button, file_name_label, \
           format_prev_button, format_next_button

