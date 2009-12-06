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
Hildon UI. Widgets for sync mode.
"""

import gtk

def create_sync_ui(main_switcher):
    """Creates SyncWidget UI."""

    toplevel_table = gtk.Table(rows=1, columns=2)
    toolbar_container = gtk.Notebook()
    toolbar_container.set_show_tabs(False)
    toolbar_container.set_size_request(82, 480)
    toolbar_container.set_name('three_button_container')
    toolbar_table = gtk.Table(rows=5, columns=1, homogeneous=True)
    client_mode_button = gtk.ToggleButton()
    client_mode_button.set_size_request(80, 80)
    client_mode_button.set_name('sync_toolbar_client_mode_button')
    server_mode_button = gtk.ToggleButton()
    server_mode_button.set_size_request(80, 80)
    server_mode_button.set_name('sync_toolbar_server_mode_button')
    menu_button = create_button('main_menu_button')
    role_switcher = gtk.Notebook()
    role_switcher.set_show_tabs(False)
    role_switcher.set_show_border(False)
    information_label = gtk.Label('This mode allows you to sync your ' \
        'database with another copy of Mnemosyne program. You can use it' \
        'as Server or Client.')
    information_label.set_line_wrap(True)
    information_label.set_justify(gtk.JUSTIFY_CENTER)
    information_label.set_name('white_label')
    client_table = gtk.Table(rows=2, columns=1)
    server_table = gtk.Table(rows=2, columns=1)
    client_start_button = gtk.ToggleButton()
    client_start_button.set_size_request(72, 72)
    client_start_button.set_name('sync_button')
    server_start_button = gtk.ToggleButton()
    server_start_button.set_size_request(72, 72)
    server_start_button.set_name('sync_button')
    client_box = gtk.VBox()
    client_params_table = gtk.Table(rows=4, columns=2)
    client_params_table.set_row_spacings(10)
    client_params_table.set_col_spacings(10)
    client_status_table = gtk.VBox()
    client_status_label = gtk.Label()
    client_status_label.set_name('white_label')
    client_progressbar = gtk.ProgressBar()
    client_progressbar.set_name('sync_mode_client_progressbar')
    client_login_label = gtk.Label('Login:')
    client_login_label.set_name('white_label')
    client_passwd_label = gtk.Label('Password:')
    client_passwd_label.set_name('white_label')
    client_address_label = gtk.Label('Server address:')
    client_address_label.set_name('white_label')
    client_port_label = gtk.Label('Server port:')
    client_port_label.set_name('white_label')
    client_login_entry_container = gtk.Frame()
    client_login_entry_container.set_name('html_container')
    client_passwd_entry_container = gtk.Frame()
    client_passwd_entry_container.set_name('html_container')
    client_address_entry_container = gtk.Frame()
    client_address_entry_container.set_name('html_container')
    client_port_entry_container = gtk.Frame()
    client_port_entry_container.set_name('html_container')
    client_login_entry = gtk.Entry()
    client_login_entry.set_name('entry_widget')
    client_passwd_entry = gtk.Entry()
    client_passwd_entry.set_name('entry_widget')
    client_address_entry = gtk.Entry()
    client_address_entry.set_name('entry_widget')
    client_port_entry = gtk.Entry()
    client_port_entry.set_name('entry_widget')
    server_box = gtk.VBox()
    server_params_table = gtk.Table(rows=4, columns=2)
    server_params_table.set_row_spacings(10)
    server_params_table.set_col_spacings(10)
    server_status_table = gtk.VBox()
    server_status_label = gtk.Label()
    server_status_label.set_name('white_label')
    server_progressbar = gtk.ProgressBar()
    server_progressbar.set_name('sync_mode_server_progressbar')
    server_login_label = gtk.Label('Login:')
    server_login_label.set_name('white_label')
    server_passwd_label = gtk.Label('Password:')
    server_passwd_label.set_name('white_label')
    server_address_label = gtk.Label('IP address:')
    server_address_label.set_name('white_label')
    server_port_label = gtk.Label('Port:')
    server_port_label.set_name('white_label')
    server_login_entry_container = gtk.Frame()
    server_login_entry_container.set_name('html_container')
    server_passwd_entry_container = gtk.Frame()
    server_passwd_entry_container.set_name('html_container')
    server_address_entry_container = gtk.Frame()
    server_address_entry_container.set_name('html_container')
    server_port_entry_container = gtk.Frame()
    server_port_entry_container.set_name('html_container')
    server_login_entry = gtk.Entry()
    server_login_entry.set_name('entry_widget')
    server_passwd_entry = gtk.Entry()
    server_passwd_entry.set_name('entry_widget')
    server_address_entry = gtk.Entry()
    server_address_entry.set_name('entry_widget')
    server_port_entry = gtk.Entry()
    server_port_entry.set_name('entry_widget')
    # packing widgets
    toolbar_table.attach(client_mode_button, 0, 1, 0, 1, \
        xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
    toolbar_table.attach(server_mode_button, 0, 1, 1, 2, \
        xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
    toolbar_table.attach(menu_button, 0, 1, 4, 5, \
        xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
    toolbar_container.add(toolbar_table)
    toplevel_table.attach(toolbar_container, 0, 1, 0, 1, \
        xoptions=gtk.SHRINK, yoptions=gtk.EXPAND|gtk.FILL|gtk.SHRINK)
    role_switcher.append_page(information_label)
    client_login_entry_container.add(client_login_entry)
    client_passwd_entry_container.add(client_passwd_entry)
    client_address_entry_container.add(client_address_entry)
    client_port_entry_container.add(client_port_entry)
    client_params_table.attach(client_login_label, 0, 1, 0, 1, \
        xoptions=gtk.SHRINK, yoptions=gtk.SHRINK)
    client_params_table.attach(client_login_entry_container, 1, 2, 0, 1, \
        xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL)
    client_params_table.attach(client_passwd_label, 0, 1, 1, 2, \
        xoptions=gtk.SHRINK, yoptions=gtk.SHRINK)
    client_params_table.attach(client_passwd_entry_container, 1, 2, 1, 2, \
        xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL)
    client_params_table.attach(client_address_label, 0, 1, 2, 3, \
        xoptions=gtk.SHRINK, yoptions=gtk.SHRINK)
    client_params_table.attach(client_address_entry_container, 1, 2, 2, 3, \
        xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL)
    client_params_table.attach(client_port_label, 0, 1, 3, 4, \
        xoptions=gtk.SHRINK, yoptions=gtk.SHRINK)
    client_params_table.attach(client_port_entry_container, 1, 2, 3, 4, \
        xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL)
    client_status_table.pack_start(client_status_label, expand=False, \
        fill=False)
    client_status_table.pack_end(client_progressbar, expand=False, \
        fill=False)
    client_box.pack_start(client_params_table, expand=False, fill=True)
    client_box.pack_end(client_status_table, expand=True, fill=True)
    client_table.attach(client_start_button, 0, 1, 1, 2, \
        xoptions=gtk.EXPAND, yoptions=gtk.SHRINK, ypadding=4)
    client_table.attach(client_box, 0, 1, 0, 1, \
        xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL)
    role_switcher.append_page(client_table)
    server_login_entry_container.add(server_login_entry)
    server_passwd_entry_container.add(server_passwd_entry)
    server_address_entry_container.add(server_address_entry)
    server_port_entry_container.add(server_port_entry)
    server_params_table.attach(server_login_label, 0, 1, 0, 1, \
        xoptions=gtk.SHRINK, yoptions=gtk.SHRINK)
    server_params_table.attach(server_login_entry_container, 1, 2, 0, 1, \
        xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL)
    server_params_table.attach(server_passwd_label, 0, 1, 1, 2, \
        xoptions=gtk.SHRINK, yoptions=gtk.SHRINK)
    server_params_table.attach(server_passwd_entry_container, 1, 2, 1, 2, \
        xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL)
    server_params_table.attach(server_address_label, 0, 1, 2, 3, \
        xoptions=gtk.SHRINK, yoptions=gtk.SHRINK)
    server_params_table.attach(server_address_entry_container, 1, 2, 2, 3, \
        xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL)
    server_params_table.attach(server_port_label, 0, 1, 3, 4, \
        xoptions=gtk.SHRINK, yoptions=gtk.SHRINK)
    server_params_table.attach(server_port_entry_container, 1, 2, 3, 4, \
        xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL)
    server_status_table.pack_start(server_status_label, expand=False, \
        fill=False)
    server_status_table.pack_end(server_progressbar, expand=False, \
        fill=False)
    server_box.pack_start(server_params_table, expand=False, fill=True)
    server_box.pack_end(server_status_table, expand=True, fill=True)
    server_table.attach(server_start_button, 0, 1, 1, 2, \
        xoptions=gtk.EXPAND, yoptions=gtk.SHRINK, ypadding=4)
    server_table.attach(server_box, 0, 1, 0, 1, \
        xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL)
    role_switcher.append_page(server_table)
    toplevel_table.attach(role_switcher, 1, 2, 0, 1, xpadding=14, \
        ypadding=14, xoptions=gtk.EXPAND|gtk.FILL|gtk.SHRINK, \
        yoptions=gtk.EXPAND|gtk.FILL|gtk.SHRINK)
    toplevel_table.show_all()
    # hide necessary widgets
    client_status_table.hide()
    server_status_table.hide()
    return main_switcher.append_page(toplevel_table), client_progressbar, \
        server_progressbar, client_start_button, server_start_button, \
        role_switcher, client_mode_button, server_mode_button, \
        client_status_label, server_status_label, client_login_entry, \
        client_passwd_entry, client_address_entry, client_port_entry, \
        server_login_entry, server_passwd_entry, server_address_entry, \
        server_port_entry, menu_button, client_params_table, \
        server_params_table


