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
Hildon UI. Menu widgets.
"""

import gtk
from mnemosyne.libmnemosyne.ui_component import UiComponent

class MenuWidget(UiComponent):
    """Main menu widget."""

    component_type = "menu_widget"

    def __init__(self, component_manager):
        UiComponent.__init__(self, component_manager)
        self._main_widget = self.main_widget()
        # create widgets
        toplevel_table = gtk.Table(rows=2, columns=1)
        app_name_label = gtk.Label('Mnemosyne for Maemo')
        app_name_label.set_name('program_name_label')
        buttons_table = gtk.Table(rows=2, columns=1)
        buttons_table.set_row_spacings(14)
        row1 = gtk.Table(rows=1, columns=6)
        row1.set_col_spacings(14)
        row2 = gtk.Table(rows=1, columns=5)
        row2.set_col_spacings(14)
        buttons = {}
        for button_name in ('tags', 'review', 'input', 'settings', 'sync', \
            'about', 'exit'):
            button = gtk.Button()
            button.set_size_request(110, 155)
            button.set_name('menu_button_%s' % button_name)
            button.connect('clicked', getattr(self, '%s_cb' % button_name))
            button_table = gtk.Table(rows=4, columns=1, homogeneous=True)
            button_label = gtk.Label(button_name.capitalize())
            button_label.set_name('menu_label_%s' % button_name)
            button_table.attach(button_label, 0, 1, 3, 4)
            button.add(button_table)
            buttons[button_name] = button
        # packing
        row1.attach(buttons['tags'], 1, 2, 0, 1)
        row1.attach(buttons['review'], 2, 3, 0, 1)
        row1.attach(buttons['input'], 3, 4, 0, 1)
        row1.attach(buttons['settings'], 4, 5, 0, 1)
        row2.attach(buttons['sync'], 1, 2, 0, 1)
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
        self._main_widget.switcher.insert_page(toplevel_table, position=0)

    def activate(self):
        """Activates necessary switcher page."""
        self._main_widget.switcher.set_current_page(0)

    # callbacks
    def tags_cb(self, widget):
        """Go to activate tags mode."""
        self._main_widget.tags_()

    def input_cb(self, widget):
        """Go to input mode."""
        self._main_widget.input_()

    def review_cb(self, widget):
        """Go to review mode."""
        self._main_widget.review_()

    def sync_cb(self, widget):
        """Go to sync mode."""
        self._main_widget.sync_()

    def settings_cb(self, widget):
        """Go to configuration mode."""
        self._main_widget.configure_()

    def about_cb(self, widget):
        """Go to about mode."""
        self._main_widget.about_()

    def exit_cb(self, widget):
        """Exit program."""
        self._main_widget.exit_()


# Local Variables:
# mode: python
# py-indent-offset: 4
# indent-tabs-mode nil
# tab-width 4
# End:
