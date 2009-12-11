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

def create_statistics_ui(main_switcher, statistics_text):
    """Creates MaemoStatisticsWidget UI."""

    toplevel_table = gtk.Table(rows=1, columns=2)
    toolbar_container = gtk.Notebook()
    toolbar_container.set_show_tabs(False)
    toolbar_container.set_size_request(82, 480)
    toolbar_container.set_name('one_button_container')
    toolbar_table = gtk.Table(rows=5, columns=1, homogeneous=True)
    menu_button = gtk.Button()
    menu_button.set_size_request(80, 80)
    menu_button.set_name('main_menu_button')
    info_container = gtk.Notebook()
    info_container.set_show_border(False)
    info_container.set_show_tabs(False)
    info_box = gtk.VBox()
    label_title = gtk.Label()
    label_title.set_use_markup(True)
    label_title.set_justify(gtk.JUSTIFY_CENTER)
    label_title.set_markup("<span foreground='white' size='x-large'><b>"\
        "Current card statistics</b></span>")
    label_text = gtk.Label()
    label_text.set_use_markup(True)
    label_text.set_justify(gtk.JUSTIFY_LEFT)
    label_text.set_markup(statistics_text)
    info_box.pack_start(label_title, expand=False, fill=True, padding=10)
    info_box.pack_start(label_text, expand=False, fill=True, padding=10)
    info_container.append_page(info_box)
    toolbar_table.attach(menu_button, 0, 1, 4, 5, xoptions=gtk.EXPAND, \
        yoptions=gtk.EXPAND)
    toolbar_container.append_page(toolbar_table)
    toplevel_table.attach(toolbar_container, 0, 1, 0, 1, \
        xoptions=gtk.SHRINK, yoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL)
    toplevel_table.attach(info_container, 1, 2, 0, 1, \
        xoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL, \
        yoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL)
    toplevel_table.show_all()
    return main_switcher.append_page(toplevel_table), menu_button


