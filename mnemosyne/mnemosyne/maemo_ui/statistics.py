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
Hildon UI. Statistics widget.
"""

from mnemosyne.libmnemosyne.ui_components.dialogs import StatisticsDialog
from mnemosyne.maemo_ui.widgets.statistics import create_statistics_ui
from mnemosyne.libmnemosyne.statistics import CurrentCardStatisctcs

DAY = 24 * 60 * 60 # Seconds in a day.

class MaemoStatisticsWidget(StatisticsDialog):
    """Statistics Widget."""

    def __init__(self, component_manager, previous_mode=None):
        self.statistics_text = ""
        self.component_manager = component_manager
        StatisticsDialog.__init__(self, component_manager)
        self.prepare_statistics()
        # create widgets
        self.page, menu_button = create_statistics_ui(\
            self.main_widget().switcher, self.statistics_text)
        # connect signals
        if previous_mode == 'Menu':
            menu_button.connect('clicked', self.back_to_main_menu_cb)
        else:
            menu_button.connect('clicked', self.back_to_previous_mode_cb)

    def prepare_statistics(self):
        """Preparing statistics text"""
        
        data = CurrentCardStatisctcs(self.component_manager).get_data()
        self.statistics_text = """<span  foreground='white'\
        size="x-large">"""
        if data.has_key('error'):
            self.statistics_text += data['error']
        else:
            self.statistics_text += "\n".join(["%s %s" % (name, result) \
                                        for name, result in data.items()])
        self.statistics_text += "</span>"


    def activate(self):
        """Set necessary switcher page."""

        self.main_widget().switcher.set_current_page(self.page)

    def back_to_previous_mode_cb(self, widget):
        """Returns to previous menu."""

        self.main_widget().switcher.remove_page(self.page)

    def back_to_main_menu_cb(self, widget):
        """Returns to main menu."""

        self.main_widget().switcher.remove_page(self.page)
        self.main_widget().menu_('statistics')

