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
Hildon UI. Widgets for about mode.
"""

import gtk

def create_about_ui(main_switcher, image_name):
    """Creates AboutWidget UI."""

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
    hbutton_box = gtk.HButtonBox()
    text_box = gtk.HBox()
    logo_box = gtk.HBox()
    label_left = gtk.Label()
    label_left.set_use_markup(True)
    label_left.set_markup("<span foreground='white' size='small'><b>" \
        "Developers:</b></span>\n<span foreground='white' size='small'>" \
        "Max Usachev |</span> <span foreground='#299BFC' size='small'>" \
        "maxusachev@gmail.com</span>\n<span foreground='white' size=" \
        "'small'>Ed Bartosh |</span> <span foreground='#299BFC' size=" \
        "'small'>bartosh@gmail.com</span>\n<span foreground='white' " \
        "size='small'>Vlad Vasiliev |</span> <span foreground='#299BFC' " \
        "size='small'>vlad@gas.by</span>\n\n<span foreground='white' " \
        "size='small'><b>Designer:</b>\n</span><span foreground='white' " \
        "size='small'>Andrew Zhilin |</span> <span foreground='#299BFC' " \
        "size='small'>drew.zhilin@gmail.com</span>\n\n<span foreground=" \
        "'white' size='small'><b>Development team:</b></span>\n<span " \
        "foreground='#299BFC' size='small'>pomni@googlegroups.com</span>")
    label_right = gtk.Label()
    label_right.set_use_markup(True)
    label_right.set_markup("<span foreground='white' size='small'><b>" \
        "Special Thanks To:</b></span>\n<span foreground='white' size=" \
        "'small'>Peter Bienstman</span>\n<span foreground='#299BFC' size=" \
        "'small'>Peter.Bienstman@ugent.be</span>\n<span foreground=" \
        "'#299BFC' size='small'>http://www.mnemosyne-proj.org/</span>" \
        "\n<span size='x-large'></span><span foreground='white' size=" \
        "'small'>\nGSoC 2009</span>\n<span foreground='#299BFC' size='"\
        "small'>http://socghop.appspot.com/</span>\n\n<span size='x-large'>" \
        "</span><span foreground='white' size='small'>\nMaemo community" \
        "</span>\n<span foreground='#299BFC' size='small'>" \
        "http://maemo.org/</span>")
    logo = gtk.Image()
    logo.set_from_file(image_name)
    program_label = gtk.Label()
    program_label.set_justify(gtk.JUSTIFY_CENTER)
    program_label.set_use_markup(True)
    program_label.set_markup("<span foreground='white' size='large'><b>" \
        "Mnemosyne for Maemo</b></span>\n<span foreground='white' size=" \
        "'large'>version 2.0.0 beta6</span>")
    # packing widgets
    logo_box.pack_start(logo, expand=False, fill=False, padding=10)
    logo_box.pack_end(program_label, expand=False, fill=False)
    hbutton_box.pack_start(logo_box)
    text_box.pack_start(label_left)
    text_box.pack_end(label_right)
    info_box.pack_start(hbutton_box, expand=False)
    info_box.pack_end(text_box)
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


