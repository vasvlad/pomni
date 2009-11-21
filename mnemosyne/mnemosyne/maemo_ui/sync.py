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
Hildon UI. Sync Widget.
"""

import gtk
import sys
sys.path.insert(0, "../../")
sys.path.insert(0, "../")

import socket
from libSM2sync.server import Server
from libSM2sync.client import Client
from libSM2sync.sync import UIMessenger
from mnemosyne.maemo_ui.widgets import BaseHildonWidget


class SyncWidget(BaseHildonWidget):
    """Sync Widget."""

    def __init__(self, component_manager):
        BaseHildonWidget.__init__(self, component_manager)
        self.client = None
        self.server = None
        self.db_path = None
        self.server_thread = None
        self.conf = self.config()

        # create widgets
        toplevel_table = gtk.Table(rows=1, columns=2)
        toolbar_container = self.create_toolbar_container( \
            'sync_mode_toolbar_container')
        toolbar_table = gtk.Table(rows=5, columns=1, homogeneous=True)
        client_mode_button = gtk.ToggleButton()
        client_mode_button.set_size_request(80, 80)
        client_mode_button.connect('pressed', self.activate_client_mode_cb)
        client_mode_button.set_name('sync_toolbar_client_mode_button')
        server_mode_button = gtk.ToggleButton()
        server_mode_button.set_size_request(80, 80)
        server_mode_button.connect('pressed', self.activate_server_mode_cb)
        server_mode_button.set_name('sync_toolbar_server_mode_button')
        menu_button = self.create_button('sync_toolbar_main_menu_button', \
            self.sync_to_main_menu_cb)
        role_switcher = gtk.Notebook()
        role_switcher.set_show_tabs(False)
        role_switcher.set_show_border(False)
        information_label = gtk.Label('This mode allows you to sync your ' \
            'database with another copy of Mnemosyne program. You can use it' \
            'as Server or Client.')
        information_label.set_line_wrap(True)
        information_label.set_justify(gtk.JUSTIFY_CENTER)
        information_label.set_name('sync_mode_information_label')
        client_table = gtk.Table(rows=2, columns=1)
        server_table = gtk.Table(rows=2, columns=1)
        client_start_button = gtk.ToggleButton()
        client_start_button.set_size_request(72, 72)
        client_start_button.connect('pressed', self.start_client_sync_cb)
        client_start_button.set_name('sync_mode_client_start_button')
        server_start_button = gtk.ToggleButton()
        server_start_button.set_size_request(72, 72)
        server_start_button.connect('pressed', self.start_server_sync_cb)
        server_start_button.set_name('sync_mode_server_start_button')
        client_box = gtk.VBox()
        client_params_table = gtk.Table(rows=4, columns=2)
        client_params_table.set_row_spacings(10)
        client_params_table.set_col_spacings(10)
        client_status_table = gtk.VBox()
        client_status_label = gtk.Label()
        client_status_label.set_name('sync_mode_client_status_label')
        client_progressbar = gtk.ProgressBar()
        client_progressbar.set_name('sync_mode_client_progressbar')
        client_login_label = gtk.Label('Login:')
        client_login_label.set_name('sync_mode_client_login_label')
        client_passwd_label = gtk.Label('Password:')
        client_passwd_label.set_name('sync_mode_client_passwd_label')
        client_address_label = gtk.Label('Server address:')
        client_address_label.set_name('sync_mode_client_address_label')
        client_port_label = gtk.Label('Server port:')
        client_port_label.set_name('sync_mode_client_port_label')
        client_login_entry_container = gtk.Frame()
        client_login_entry_container.set_name( \
            'sync_mode_client_login_entry_container')
        client_passwd_entry_container = gtk.Frame()
        client_passwd_entry_container.set_name( \
            'sync_mode_client_passwd_entry_container')
        client_address_entry_container = gtk.Frame()
        client_address_entry_container.set_name( \
            'sync_mode_client_address_entry_container')
        client_port_entry_container = gtk.Frame()
        client_port_entry_container.set_name( \
            'sync_mode_client_port_entry_container')
        client_login_entry = gtk.Entry()
        client_login_entry.set_name('sync_mode_client_login_entry')
        client_passwd_entry = gtk.Entry()
        client_passwd_entry.set_name('sync_mode_client_passwd_entry')
        client_address_entry = gtk.Entry()
        client_address_entry.set_name('sync_mode_client_address_entry')
        client_port_entry = gtk.Entry()
        client_port_entry.set_name('sync_mode_client_port_entry')
        server_box = gtk.VBox()
        server_params_table = gtk.Table(rows=4, columns=2)
        server_params_table.set_row_spacings(10)
        server_params_table.set_col_spacings(10)
        server_status_table = gtk.VBox()
        server_status_label = gtk.Label()
        server_status_label.set_name('sync_mode_server_status_label')
        server_progressbar = gtk.ProgressBar()
        server_progressbar.set_name('sync_mode_server_progressbar')
        server_login_label = gtk.Label('Login:')
        server_login_label.set_name('sync_mode_server_login_label')
        server_passwd_label = gtk.Label('Password:')
        server_passwd_label.set_name('sync_mode_server_passwd_label')
        server_address_label = gtk.Label('IP address:')
        server_address_label.set_name('sync_mode_server_address_label')
        server_port_label = gtk.Label('Port:')
        server_port_label.set_name('sync_mode_server_port_label')
        server_login_entry_container = gtk.Frame()
        server_login_entry_container.set_name( \
            'sync_mode_server_login_entry_container')
        server_passwd_entry_container = gtk.Frame()
        server_passwd_entry_container.set_name( \
            'sync_mode_server_passwd_entry_container')
        server_address_entry_container = gtk.Frame()
        server_address_entry_container.set_name( \
            'sync_mode_server_address_entry_container')
        server_port_entry_container = gtk.Frame()
        server_port_entry_container.set_name( \
            'sync_mode_server_port_entry_container')
        server_login_entry = gtk.Entry()
        server_login_entry.set_name('sync_mode_server_login_entry')
        server_passwd_entry = gtk.Entry()
        server_passwd_entry.set_name('sync_mode_server_passwd_entry')
        server_address_entry = gtk.Entry()
        server_address_entry.set_name('sync_mode_server_address_entry')
        server_port_entry = gtk.Entry()
        server_port_entry.set_name('sync_mode_server_port_entry')
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
        self.page = self.main_widget().switcher.append_page(toplevel_table)
        # create attributes
        self.client_progressbar = client_progressbar
        self.server_progressbar = server_progressbar
        self.client_start_button = client_start_button
        self.server_start_button = server_start_button
        self.role_switcher = role_switcher
        self.client_mode_button = client_mode_button
        self.server_mode_button = server_mode_button
        self.client_status_label = client_status_label
        self.server_status_label = server_status_label
        self.client_login_entry = client_login_entry
        self.client_passwd_entry = client_passwd_entry
        self.client_address_entry = client_address_entry
        self.client_port_entry = client_port_entry
        self.server_login_entry = server_login_entry
        self.server_passwd_entry = server_passwd_entry
        self.server_address_entry = server_address_entry
        self.server_port_entry = server_port_entry
        self.menu_button = menu_button
        self.client_table = client_params_table
        self.server_table = server_params_table

    def complete_events(self):
        """Defreeze GTK UI."""

        while gtk.events_pending():
            gtk.main_iteration(False)

    def activate(self):
        """Activate sync mode."""

        self.main_widget().switcher.set_current_page(self.page)
        self.role_switcher.set_current_page(0)
        self.client_mode_button.set_active(False)
        self.server_mode_button.set_active(False)

    def activate_client_mode_cb(self, widget):
        """Switches to Client mode."""

        self.server_mode_button.set_active(False)
        self.role_switcher.set_current_page(1)

    def activate_server_mode_cb(self, widget):
        """Switches to Server mode."""

        self.client_mode_button.set_active(False)
        self.role_switcher.set_current_page(2)

    def update_client_progressbar(self, fraction):
        """Updates client progress bar indicator."""

        self.client_progressbar.set_fraction(fraction)
        self.complete_events()

    def update_server_progressbar(self, fraction):
        """Updates server progress bar indicator."""

        self.server_progressbar.set_fraction(fraction)
        self.complete_events()

    def show_message(self, message):
        """Show message from Client or Server."""

        self.main_widget().information_box(message)
        self.complete_events()

    def update_client_status(self, text):
        """Set client status text."""

        status_label = self.client_status_label
        status_label.set_text(text)
        status_label.show()
        self.complete_events()
   
    def update_server_status(self, text):
        """Set server status text."""

        status_label = self.server_status_label
        status_label.set_text(text)
        status_label.show()
        self.complete_events()

    def start_client_sync_cb(self, widget):
        """Starts syncing as Client."""

        if not widget.get_active():
            self.show_or_hide_containers(False, "client")
            login = self.client_login_entry.get_text()
            passwd = self.client_passwd_entry.get_text()
            host = self.client_address_entry.get_text()
            port = self.client_port_entry.get_text()
            uri = host + ':' + port
            if not uri.startswith("http://"):
                uri = "http://" + uri
            messenger = UIMessenger(self.show_message, self.complete_events, \
                self.update_client_status, self.client_progressbar.show, \
                self.update_client_progressbar, self.client_progressbar.hide)
            self.client = Client(host, port, uri, self.database(), \
                self.controller(), self.config(), self.log(), messenger)
            self.client.set_user(login, passwd)
            self.complete_events()
            self.client.start()
            self.show_or_hide_containers(True, "client")
            self.client_start_button.set_active(False)
        else:
            self.show_or_hide_containers(True, "client")
            self.client.stop()
            self.client = None

    def start_server_sync_cb(self, widget):
        """Starts syncing as Server."""

        if not widget.get_active():
            try:
                port = int(self.server_port_entry.get_text())
            except ValueError:
                self.main_widget().error_box("Wrong port number!")
            else:
                host = self.server_address_entry.get_text()
                self.show_or_hide_containers(False, "server")
                try:
                    messenger = UIMessenger(self.show_message, \
                    self.complete_events, self.update_server_status, \
                    self.server_progressbar.show, \
                    self.update_server_progressbar, \
                    self.server_progressbar.hide)
                    self.server = Server("%s:%s" % (host, port), \
                    self.database(), self.config(), self.log(), messenger)
                except socket.error, error:
                    self.show_message(str(error))
                else:
                    self.server.set_user( \
                        self.server_login_entry.get_text(),
                        self.server_passwd_entry.get_text())
                    self.server.start()
                self.show_or_hide_containers(True, "server")
                self.server_start_button.set_active(False)
        else:
            self.show_or_hide_containers(True, "server")
            self.server.stop()
            self.server = None

    def show_or_hide_containers(self, show, name):
        """Manages containers."""

        if show:
            getattr(self, "%s_table" % name).show()
            getattr(self, "%s_table" % name).hide()
        else:
            getattr(self, "%s_table" % name).hide()
            getattr(self, "%s_table" % name).show()
        self.client_mode_button.set_sensitive(show)
        self.server_mode_button.set_sensitive(show)
        self.menu_button.set_sensitive(show)

    def sync_to_main_menu_cb(self, widget):
        """Returns to main menu."""

        self.conf['client_login'] = self.client_login_entry.get_text()
        self.conf['client_passwd'] = self.client_passwd_entry.get_text()
        self.conf['client_sync_address'] = self.client_address_entry.get_text()
        self.conf['client_sync_port'] = self.client_port_entry.get_text()
        self.conf['server_login'] = self.server_login_entry.get_text()
        self.conf['server_passwd'] = self.server_passwd_entry.get_text()
        self.conf['server_sync_port'] = self.server_port_entry.get_text()
        self.conf['server_sync_address'] = self.server_address_entry.get_text()
        self.conf.save()
        self.main_widget().switcher.remove_page(self.page)
        self.main_widget().menu_('sync')
       
