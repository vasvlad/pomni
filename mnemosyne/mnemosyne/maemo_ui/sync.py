#!/usr/bin/python -tt7
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

from libSM2sync.server import Server
from libSM2sync.client import Client
from mnemosyne.libmnemosyne.ui_component import UiComponent

class SyncWidget(UiComponent):
    """Sync Widget."""

    def __init__(self, component_manager):
        UiComponent.__init__(self, component_manager)
        self.client = self.server = None
        self.w_tree = self.main_widget().w_tree
        self.w_tree.signal_autoconnect(\
            dict([(sig, getattr(self, sig + "_cb")) for sig in \
                ("sync_to_main_menu", "activate_client_mode", \
                "activate_server_mode", "start_client_sync", \
                "start_server_sync")]))
        self.conf = self.config()
        self.get_widget = self.w_tree.get_widget
        self.get_widget(\
            "sync_mode_client_login_entry").set_text(self.conf['login'])
        self.get_widget(\
            "sync_mode_client_passwd_entry").set_text(self.conf['user_passwd'])

    def complete_events(self):
        while gtk.events_pending():
            gtk.main_iteration(False)

    def activate(self):
        """Activate sync mode."""

        self.get_widget("sync_mode_role_switcher").set_current_page(1)
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

    def update_progress_bar(self, fraction):
        """Updates progress bar indicator."""

        self.get_widget("sync_mode_client_progressbar").set_fraction(fraction)

    def show_message(self, message):
        """Show message from Client."""

        self.main_widget().information_box(message)
   
    def start_client_sync_cb(self, widget):
        """Starts syncing as Client."""

        if not widget.get_active():
            self.show_or_hide_containers(False, "client")
            login = self.get_widget("sync_mode_client_login_entry").get_text()
            passwd = self.get_widget("sync_mode_client_passwd_entry").get_text()
            uri = self.get_widget("sync_mode_client_address_entry").get_text()
            if not uri.startswith("http://"):
                uri = "http://" + uri
            self.complete_events()
            self.client = Client(uri, self.database(), self.controller(), \
                self.config(), self.log())
            self.client.uri = uri
            self.client.set_user(login, passwd)
            self.client.set_messenger(self.show_message)
            self.client.set_progress_bar_updater(self.update_progress_bar)
            self.client.start()
            self.show_or_hide_containers(True, "client")
            self.get_widget(\
                "sync_mode_client_start_button").set_active(False)
        else:
            self.show_or_hide_containers(True, "client")
            #self.client.stop()
            del self.client

    def start_server_sync_cb(self, widget):
        """Starts syncing as Server."""

        if not widget.get_active():
            try:
                port = self.get_widget(\
                    "sync_mode_server_port_entry").get_text()
            except ValueError:
                self.main_widget().error_box("Wrong port number!")
            else:
                self.show_or_hide_containers(False, "server")
                self.complete_evens()
                #self.server = Server("localhost:" + port, self.database(), \
                #    self.config(), self.log())
                #self.server.start()
                self.show_or_hide_containers(True, "server")
        else:
            self.show_or_hide_containers(True, "server")
            self.server.stop()

    def show_or_hide_containers(self, show, name):
        """Manages containers."""

        if show:
            self.get_widget("sync_mode_%s_params_table" % name).show()
            self.get_widget("sync_mode_%s_progressbar" % name).hide()
        else:
            self.get_widget("sync_mode_%s_params_table" % name).hide()
            self.get_widget("sync_mode_%s_progressbar" % name).show()
        self.get_widget("sync_toolbar_client_mode_button").set_sensitive(show)
        self.get_widget("sync_toolbar_server_mode_button").set_sensitive(show)
        self.get_widget("sync_toolbar_main_menu_button").set_sensitive(show)

    def sync_to_main_menu_cb(self, widget):
        """Returns to main menu."""

        self.main_widget().menu_()
       

import time
class Test:
    def __init__(self, events_updater, progress_updater):
        self.stopped = False
        self.events_updater = events_updater
        self.progress_updater = progress_updater

    def start(self):
        size = 30
        for i in range(size):
            if not self.stopped:
                time.sleep(1)
                self.events_updater()
                self.progress_updater((i+1)/float(size))
            else:
                break

    def stop(self):
        self.stopped = True
