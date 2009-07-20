#!/usr/bin/python -tt7
# vim: sw=4 ts=4 expandtab ai
#
# Pomni. Learning tool based on spaced repetition technique
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

from mnemosyne.libmnemosyne.ui_component import UiComponent

class MenuWidget(UiComponent):
    """Main menu widget."""

    component_type = "menu_widget"
    review, input, configuration = range(1, 4)

    def __init__(self, component_manager):
        UiComponent.__init__(self, component_manager)

        self.w_tree = self.main_widget().w_tree
        self.switcher = self.main_widget().switcher

        self.w_tree.signal_autoconnect(\
            dict([(mode, getattr(self, mode + "_cb")) \
                for mode in ["input", "review", "configure", "exit", "sync"]]))

    # callbacks
    def input_cb(self, widget):
        """Return to main menu."""
        self.main_widget().input_()

    def review_cb(self, widget):
        """Go to review mode."""
        self.main_widget().review_()

    def sync_cb(self, widget):
        # test xml generation in EventManager
        from libSM2sync.sync import EventManager
        em = EventManager(self.database())
        em.get_events()

    def configure_cb(self, widget):
        """Go to configuration mode."""
        self.main_widget().configure_()

    def exit_cb(self, widget):
        """Exit program."""
        self.main_widget().exit_()


# Local Variables:
# mode: python
# py-indent-offset: 4
# indent-tabs-mode nil
# tab-width 4
# End:
