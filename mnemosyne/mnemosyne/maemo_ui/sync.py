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

    def activate(self):
        """Activate sync mode."""
        print "sync activated"
