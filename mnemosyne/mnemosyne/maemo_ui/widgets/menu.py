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
Hildon UI. Widgets for menu.
"""

import gtk

def create_menu_ui(main_switcher):
    """Creates MenuWidget UI."""

    toplevel_table = gtk.Table(rows=2, columns=1)
    app_name_label = gtk.Label('Mnemosyne for Maemo')
    app_name_label.set_name('program_name_label')
    buttons_table = gtk.Table(rows=2, columns=1)
    buttons_table.set_row_spacings(14)
    row1 = gtk.Table(rows=1, columns=5)
    row1.set_col_spacings(28)
    row2 = gtk.Table(rows=1, columns=5)
    row2.set_col_spacings(28)
    buttons = {}
    for button_name in ('tags', 'review', 'input', 'settings', \
        'about', 'exit'):
        button = gtk.Button()
        button.set_size_request(110, 155)
        button.set_name('menu_button_%s' % button_name)
        button_table = gtk.Table(rows=4, columns=1, homogeneous=True)
        button_label = gtk.Label(button_name.capitalize())
        button_label.set_name('menu_label_%s' % button_name)
        button_table.attach(button_label, 0, 1, 3, 4)
        button.add(button_table)
        buttons[button_name] = button
    # packing
    row1.attach(buttons['review'], 1, 2, 0, 1)
    row1.attach(buttons['input'], 2, 3, 0, 1)
    row1.attach(buttons['tags'], 3, 4, 0, 1)
    row2.attach(buttons['settings'], 1, 2, 0, 1)
    #row2.attach(buttons['sync'], 1, 2, 0, 1)
    row2.attach(buttons['about'], 2, 3, 0, 1)
    row2.attach(buttons['exit'], 3, 4, 0, 1)
    buttons_table.attach(row1, 0, 1, 0, 1, xoptions=gtk.EXPAND, \
        yoptions=gtk.EXPAND)
    buttons_table.attach(row2, 0, 1, 1, 2, xoptions=gtk.EXPAND, \
        yoptions=gtk.EXPAND)
    toplevel_table.attach(app_name_label, 0, 1, 0, 1, \
        yoptions=gtk.SHRINK, ypadding=10)
    toplevel_table.attach(buttons_table, 0, 1, 1, 2, \
        xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
    toplevel_table.show_all()
    return main_switcher.append_page(toplevel_table), buttons


