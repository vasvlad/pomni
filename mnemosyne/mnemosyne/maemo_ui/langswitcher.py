#!/usr/bin/python -tt
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
Hildon UI: Language switcher.
"""

import gobject

try:
    from gnome import gconf
except ImportError:
    import gconf

from mnemosyne.libmnemosyne.component import Component

class LangSwitcher(Component):
    """Remembers language for set of widgets and saves/restores
       them when requested.
    """
    
    gconf_entry = "/apps/osso/inputmethod/int_kb_level_shifted"
    component_type = "langswitcher"

    def __init__(self, component_manager):
        Component.__init__(self, component_manager)
        self.widgets = {}
        
        # enable functionality if gconf entry exists
        self.gconf = gconf.client_get_default()
        try:
            self.current = self.gconf.get_value(self.gconf_entry)
            self.enabled = True
        except (gobject.GError, ValueError):
            self.enabled = False

    def restore_cb(self, widget, event):
        """Restore saved language if saved."""
        
        self.widgets.setdefault(widget.name, None)

        if self.enabled and self.widgets[widget.name] != None:
            self.current = self.gconf.get_value(self.gconf_entry)
            self.gconf.set_bool(self.gconf_entry, self.widgets[widget.name])
        
    def save_cb(self, widget, event):
        """Save current language."""
        if self.enabled:
            self.widgets[widget.name] = self.gconf.get_value(self.gconf_entry)
            self.gconf.set_bool(self.gconf_entry, self.current)

# Local Variables:
# mode: python
# py-indent-offset: 4
# indent-tabs-mode nil
# tab-width 4
# End:
