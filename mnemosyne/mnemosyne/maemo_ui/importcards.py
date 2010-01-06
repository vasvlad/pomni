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
Hildon UI. Import widget.
"""

from mnemosyne.maemo_ui.widgets.importcards  import create_import_ui


#class ImportWidget():
#    """Import Widget."""
#
#    def __init__(self, component_manager, previous_mode=None):
#        pass

from mnemosyne.maemo_ui.widgets.importcards.py import create_importcard_ui

DAY = 24 * 60 * 60 # Seconds in a day.

class ImportCardsWidget(StatisticsDialog):
    """Import Widget."""

    def __init__(self, component_manager ):
	self.page, menu_button, ok_button = create_importcard_ui( \
	self.main_widget().switcher)	

    def activate(self):
        """Set necessary switcher page."""

        self.main_widget().switcher.set_current_page(self.page)

    def back_to_previous_mode_cb(self, widget):
        """Returns to previous menu."""

        self.config()["last_variant_for_statistics_page"] = \
            self.mode_statistics_switcher.get_current_page()
        self.main_widget().switcher.remove_page(self.page)

    def back_to_main_menu_cb(self, widget):
        """Returns to main menu."""

        self.main_widget().switcher.remove_page(self.page)
        self.main_widget().menu_('importcard')

    def ok_button_cb(self, widget):
        """Ok """

    	from mnemosyne.libmnemosyne.file_formats.tsv import import_txt

        imported_cards = export_txt("./test/anki.txt", "test_anki") 	
	print imported_cards
      
