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
Hildon UI. Different widgets.
"""

import gtk
from mnemosyne.libmnemosyne.ui_component import UiComponent


class BaseHildonWidget(UiComponent):
    """Base widget."""

    def __init__(self, component_manager):
        UiComponent.__init__(self, component_manager)
        self.connections = []
        self.conf = self.config()
        #self.w_tree = self.main_widget().w_tree
        #self.w_tree = self.main_widget().w_tree
        #self.get_widget = self.w_tree.get_widget

    """
    def connect_signals(self, control):

        for wname, signal, callback in control:
            widget = self.get_widget(wname)
            cid = widget.connect(signal, callback)
            self.connections.append((widget, cid))

    def disconnect_signals(self):

        for widget, cid in self.connections:
            widget.disconnect(cid)
        self.connections = []

    """
    def create_button(self, name=None, callback=None, event='clicked', \
        width=80, height=80, label=None):
        """Creates gtkButton widget."""

        button = gtk.Button()
        button.set_size_request(width, height)
        if name is not None:
            button.set_name(name)
        if callback is not None:
            button.connect(event, callback)
        if label is not None:
            button.set_label(label)
        return button

    def create_radio_button(self, group=None, name=None, callback=None, \
        event='released', width=72, height=72):
        """Creates gtkRadioButton widget."""

        button = gtk.RadioButton(group)
        button.set_size_request(width, height)
        if name is not None:
            button.set_name(name)
        if callback is not None:
            button.connect(event, callback)
        return button

    def create_toolbar_container(self, name, show_tabs=False, width=82, \
        height=480):
        """Creates toolbar container."""

        container = gtk.Notebook()
        container.set_show_tabs(show_tabs)
        container.set_size_request(width, height)
        container.set_name(name)
        return container

    def create_tag_checkbox(self, name, active):
        """Create Tag item - GtkHBox with gtk.ToggleButton and gtk.Label."""

        hbox = gtk.HBox(homogeneous=False, spacing=10)
        button = gtk.ToggleButton()
        button.set_size_request(64, 64)
        button.set_active(active)
        button.set_name("tag_check")
        label = gtk.Label(name)
        label.set_name("tag_label")
        hbox.pack_start(button, False)
        hbox.pack_start(label, False)
        hbox.show_all()
        return hbox
