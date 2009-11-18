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
    review, input, configuration = range(1, 4)

    def __init__(self, component_manager):
        UiComponent.__init__(self, component_manager)
        self._main_widget = self.main_widget()
        container = self._main_widget.switcher
        #self._main_widget.w_tree.signal_autoconnect(\
        #    dict([(mode, getattr(self, mode + "_cb")) for mode in ['input', \
        #        'review', 'configure', 'exit', 'sync', 'about', 'tags']]))
        toplevel_table = gtk.Table(rows=2, columns=1)
        app_name_label = gtk.Label('Mnemosyne for Maemo')
        app_name_label.set_name('program_name_label')
        buttons_table = gtk.Table(rows=2, columns=1)
        buttons_table.set_row_spacings(14)
        row1 = gtk.Table(rows=1, columns=6)
        row1.set_col_spacings(14)
        row2 = gtk.Table(rows=1, columns=5)
        row2.set_col_spacings(14)
        # tags button
        tags_button = gtk.Button()
        tags_button.set_size_request(110, 155)
        tags_button.set_name('menu_button_tags')
        tags_button.connect('clicked', self.tags_cb)
        tags_button_table = gtk.Table(rows=4, columns=1, homogeneous=True)
        tags_button_label = gtk.Label('Tags')
        tags_button_label.set_name('menu_label_tags')
        # review button
        review_button = gtk.Button()
        review_button.set_size_request(110, 155)
        review_button.set_name('menu_button_review')
        review_button.connect('clicked', self.review_cb)
        review_button_table = gtk.Table(rows=4, columns=1, homogeneous=True)
        review_button_label = gtk.Label('Review')
        review_button_label.set_name('menu_label_review')
        # input button
        input_button = gtk.Button()
        input_button.set_size_request(110, 155)
        input_button.set_name('menu_button_input')
        input_button.connect('clicked', self.input_cb)
        input_button_table = gtk.Table(rows=4, columns=1, homogeneous=True)
        input_button_label = gtk.Label('Input')
        input_button_label.set_name('menu_label_input')
        # settings button
        settings_button = gtk.Button()
        settings_button.set_size_request(110, 155)
        settings_button.set_name('menu_button_conf')
        settings_button.connect('clicked', self.configure_cb)
        settings_button_table = gtk.Table(rows=4, columns=1, homogeneous=True)
        settings_button_label = gtk.Label('Settings')
        settings_button_label.set_name('menu_label_settings')
        # sync button
        sync_button = gtk.Button()
        sync_button.set_size_request(110, 155)
        sync_button.set_name('menu_button_sync')
        sync_button.connect('clicked', self.sync_cb)
        sync_button_table = gtk.Table(rows=4, columns=1, homogeneous=True)
        sync_button_label = gtk.Label('Sync')
        sync_button_label.set_name('menu_label_sync')
        # about button
        about_button = gtk.Button()
        about_button.set_size_request(110, 155)
        about_button.set_name('menu_button_about')
        about_button.connect('clicked', self.about_cb)
        about_button_table = gtk.Table(rows=4, columns=1, homogeneous=True)
        about_button_label = gtk.Label('About')
        about_button_label.set_name('menu_label_about')
        # exit button
        exit_button = gtk.Button()
        exit_button.set_size_request(110, 155)
        exit_button.set_name('menu_button_exit')
        exit_button.connect('clicked', self.exit_cb)
        exit_button_table = gtk.Table(rows=4, columns=1, homogeneous=True)
        exit_button_label = gtk.Label('Exit')
        exit_button_label.set_name('menu_label_exit')

        # packing
        tags_button_table.attach(tags_button_label, 0, 1, 3, 4)
        tags_button.add(tags_button_table)
        review_button_table.attach(review_button_label, 0, 1, 3, 4)
        review_button.add(review_button_table)
        input_button_table.attach(input_button_label, 0, 1, 3, 4)
        input_button.add(input_button_table)
        settings_button_table.attach(settings_button_label, 0, 1, 3, 4)
        settings_button.add(settings_button_table)
        sync_button_table.attach(sync_button_label, 0, 1, 3, 4)
        sync_button.add(sync_button_table)
        about_button_table.attach(about_button_label, 0, 1, 3, 4)
        about_button.add(about_button_table)
        exit_button_table.attach(exit_button_label, 0, 1, 3, 4)
        exit_button.add(exit_button_table)
        row1.attach(tags_button, 1, 2, 0, 1)
        row1.attach(review_button, 2, 3, 0, 1)
        row1.attach(input_button, 3, 4, 0, 1)
        row1.attach(settings_button, 4, 5, 0, 1)
        row2.attach(sync_button, 1, 2, 0, 1)
        row2.attach(about_button, 2, 3, 0, 1)
        row2.attach(exit_button, 3, 4, 0, 1)
        buttons_table.attach(row1, 0, 1, 0, 1, xoptions=gtk.EXPAND, \
            yoptions=gtk.EXPAND)
        buttons_table.attach(row2, 0, 1, 1, 2, xoptions=gtk.EXPAND, \
            yoptions=gtk.EXPAND)
        toplevel_table.attach(app_name_label, 0, 1, 0, 1, yoptions=gtk.SHRINK, ypadding=10)
        toplevel_table.attach(buttons_table, 0, 1, 1, 2, xoptions=gtk.EXPAND, \
            yoptions=gtk.EXPAND)
        toplevel_table.show_all()
        container.append_page(toplevel_table)


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

    def configure_cb(self, widget):
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
