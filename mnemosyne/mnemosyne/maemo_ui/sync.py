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

from mnemosyne.libmnemosyne.ui_component import UiComponent

class SyncWidget(UiComponent):
    """Sync Widget."""

    def __init__(self, component_manager):
        UiComponent.__init__(self, component_manager)
        self.w_tree = self.main_widget().w_tree
        self.w_tree.signal_autoconnect(\
            dict([(sig, getattr(self, sig + "_cb")) for sig in \
                ("sync_to_main_menu", "activate_client_mode", \
                "activate_server_mode", "start_client_sync", \
                "start_server_sync")]))
        self.conf = self.config()
        self.w_tree.get_widget(\
            "sync_mode_client_login_entry").set_text(self.conf['login'])
        self.w_tree.get_widget(\
            "sync_mode_client_passwd_entry").set_text(self.conf['user_passwd'])

    def activate(self):
        """Activate sync mode."""

        self.w_tree.get_widget("sync_mode_role_switcher").set_current_page(0)
        self.w_tree.get_widget(\
            "sync_toolbar_client_mode_button").set_active(False)
        self.w_tree.get_widget(\
            "sync_toolbar_server_mode_button").set_active(False)

    def activate_client_mode_cb(self, widget):
        """Switches to Client mode."""

        self.w_tree.get_widget(\
            "sync_toolbar_server_mode_button").set_active(False)
        self.w_tree.get_widget("sync_mode_role_switcher").set_current_page(1)

    def activate_server_mode_cb(self, widget):
        """Switches to Server mode."""

        self.w_tree.get_widget(\
            "sync_toolbar_client_mode_button").set_active(False)
        self.w_tree.get_widget("sync_mode_role_switcher").set_current_page(2)

    def start_client_sync_cb(self, widget):
        if not widget.get_active():
            self.show_or_hide_containers(False, "client")
            # start syncing
        else:
            # stop syncing
            self.show_or_hide_containers(True, "client")

    def start_server_sync_cb(self, widget):
        if not widget.get_active():
            self.show_or_hide_containers(False, "server")
            # start syncing
        else:
            # stop syncing
            self.show_or_hide_containers(True, "server")
            
    def show_or_hide_containers(self, show, name):
        if show:
            self.w_tree.get_widget("sync_mode_%s_params_table" % name).show()
            self.w_tree.get_widget("sync_mode_%s_progress_label" % name).hide()
        else:
            self.w_tree.get_widget("sync_mode_%s_params_table" % name).hide()
            self.w_tree.get_widget("sync_mode_%s_progress_label" % name).show()
        self.w_tree.get_widget(\
            "sync_toolbar_client_mode_button").set_sensitive(show)
        self.w_tree.get_widget(\
            "sync_toolbar_server_mode_button").set_sensitive(show)
        self.w_tree.get_widget(\
            "sync_toolbar_main_menu_button").set_sensitive(show)

    def sync_to_main_menu_cb(self, widget):
        """Returns to main menu."""

        self.main_widget().menu_()
        
