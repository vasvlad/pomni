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
from mnemosyne.libmnemosyne.ui_component import UiComponent


class SyncWidget(UiComponent):
    """Sync Widget."""

    def __init__(self, component_manager):
        UiComponent.__init__(self, component_manager)
        self.client = None
        self.server = None
        self.db_path = None
        self.server_thread = None
        self.w_tree = self.main_widget().w_tree
        self.w_tree.signal_autoconnect(\
            dict([(sig, getattr(self, sig + "_cb")) for sig in \
                ("sync_to_main_menu", "activate_client_mode", \
                "activate_server_mode", "start_client_sync", \
                "start_server_sync")]))
        self.conf = self.config()
        self.get_widget = get_widget = self.w_tree.get_widget
        self.client_progressbar = get_widget("sync_mode_client_progressbar")
        self.server_progressbar = get_widget("sync_mode_server_progressbar")

        widgets_dict = {'sync_mode_client_login_entry': 'client_login', \
            'sync_mode_client_passwd_entry': 'client_passwd', \
            'sync_mode_client_address_entry': 'client_sync_address', \
            'sync_mode_client_port_entry': 'client_sync_port', \
            'sync_mode_server_login_entry': 'server_login', \
            'sync_mode_server_passwd_entry': 'server_passwd', \
            'sync_mode_server_port_entry': 'server_sync_port', \
            'sync_mode_server_address_entry': 'server_sync_address'}
        # Mandatory color setup for GtkEntry
        for widget_name, param_name in widgets_dict.items():
            get_widget(widget_name).set_text(self.conf[param_name])
            widget = get_widget(widget_name)
            widget.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("#FFFFFF"))
            widget.modify_text(gtk.STATE_NORMAL, gtk.gdk.color_parse("#000000"))

    def complete_events(self):
        """Defreeze GTK UI."""

        while gtk.events_pending():
            gtk.main_iteration(False)

    def activate(self):
        """Activate sync mode."""

        self.get_widget("sync_mode_role_switcher").set_current_page(0)
        self.get_widget("sync_toolbar_client_mode_button").set_active(False)
        self.get_widget("sync_toolbar_server_mode_button").set_active(False)

    def activate_client_mode_cb(self, widget):
        """Switches to Client mode."""

        self.get_widget("sync_toolbar_server_mode_button").set_active(False)
        self.get_widget("sync_mode_role_switcher").set_current_page(1)

    def activate_server_mode_cb(self, widget):
        """Switches to Server mode."""

        self.get_widget("sync_toolbar_client_mode_button").set_active(False)
        self.get_widget("sync_mode_role_switcher").set_current_page(2)

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

        status_label = self.get_widget("sync_mode_client_status_label")
        status_label.set_text(text)
        status_label.show()
        self.complete_events()
   
    def update_server_status(self, text):
        """Set server status text."""

        status_label = self.get_widget("sync_mode_server_status_label")
        status_label.set_text(text)
        status_label.show()
        self.complete_events()

    def start_client_sync_cb(self, widget):
        """Starts syncing as Client."""

        if not widget.get_active():
            self.show_or_hide_containers(False, "client")
            login = self.get_widget("sync_mode_client_login_entry").get_text()
            passwd = self.get_widget("sync_mode_client_passwd_entry").get_text()
            host = self.get_widget(\
                "sync_mode_client_address_entry").get_text()
            port = self.get_widget("sync_mode_client_port_entry").get_text()
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
            self.get_widget(\
                "sync_mode_client_start_button").set_active(False)
        else:
            self.show_or_hide_containers(True, "client")
            self.client.stop()
            self.client = None

    def start_server_sync_cb(self, widget):
        """Starts syncing as Server."""

        if not widget.get_active():
            try:
                port = int(self.get_widget(\
                    "sync_mode_server_port_entry").get_text())
            except ValueError:
                self.main_widget().error_box("Wrong port number!")
            else:
                host = self.get_widget(\
                    "sync_mode_server_address_entry").get_text()
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
                    self.server.set_user(\
                        self.get_widget("sync_mode_server_login_entry"). \
                            get_text(), 
                        self.get_widget("sync_mode_server_passwd_entry"). \
                            get_text())
                    self.server.start()
                self.show_or_hide_containers(True, "server")
                self.get_widget(\
                    "sync_mode_server_start_button").set_active(False)
        else:
            self.show_or_hide_containers(True, "server")
            self.server.stop()
            self.server = None

    def show_or_hide_containers(self, show, name):
        """Manages containers."""

        if show:
            self.get_widget("sync_mode_%s_params_table" % name).show()
            self.get_widget("sync_mode_%s_status_table" % name).hide()
        else:
            self.get_widget("sync_mode_%s_params_table" % name).hide()
            self.get_widget("sync_mode_%s_status_table" % name).show()
        self.get_widget("sync_toolbar_client_mode_button").set_sensitive(show)
        self.get_widget("sync_toolbar_server_mode_button").set_sensitive(show)
        self.get_widget("sync_toolbar_main_menu_button").set_sensitive(show)

    def sync_to_main_menu_cb(self, widget):
        """Returns to main menu."""

        self.conf['client_login'] = self.get_widget(\
            "sync_mode_client_login_entry").get_text()
        self.conf['client_passwd'] = self.get_widget(\
            "sync_mode_client_passwd_entry").get_text()
        self.conf['client_sync_address'] = self.get_widget(\
            "sync_mode_client_address_entry").get_text()
        self.conf['client_sync_port'] = self.get_widget(\
            "sync_mode_client_port_entry").get_text()
        self.conf['server_login'] = self.get_widget(\
            "sync_mode_server_login_entry").get_text()
        self.conf['server_passwd'] = self.get_widget(\
            "sync_mode_server_passwd_entry").get_text()
        self.conf['server_sync_port'] = self.get_widget(\
            "sync_mode_server_port_entry").get_text()
        self.conf['server_sync_address'] = self.get_widget(\
            "sync_mode_server_address_entry").get_text()
        self.conf.save()
        self.main_widget().menu_()
       
