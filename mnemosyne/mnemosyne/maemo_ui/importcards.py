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

import mnemosyne.maemo_ui.widgets.tags as widgets
from mnemosyne.libmnemosyne.ui_component import UiComponent
from mnemosyne.maemo_ui.widgets.importcards  import create_importcard_ui

class ImportCardsWidget(UiComponent):
    """Import Widget."""

    def __init__(self, component_manager ):

        UiComponent.__init__(self, component_manager)
        self.page, self.tags_box, menu_button, \
            ok_button = create_importcard_ui( \
            self.main_widget().switcher)
        self.tags_dict = {}
        # connect signals
        menu_button.connect('clicked', self.back_to_main_menu_cb)
        ok_button.connect('clicked', self.ok_button_cb)

    def activate(self):
        """Set necessary switcher page."""

        self.main_widget().switcher.set_current_page(self.page)
        self.display_criterion(self.database().current_activity_criterion())

    def display_criterion(self, criterion):
        """Display current criterion."""

        tags_box = self.tags_box
        for child in tags_box.get_children():
            tags_box.remove(child)
        for tag in self.database().get_tags():
            self.tags_dict[tag.name] = tag._id
            # get cards count for tag
            cards_count = sum([ \
                self.database().card_count_for_grade_and__tag_id( \
                    grade, tag._id) for grade in range(-1, 6)])
            tags_box.pack_start(widgets.create_tag_checkbox(tag.name + \
                unicode(" (%s cards)" % cards_count), \
                tag._id in criterion.active_tag__ids))

    def get_criterion(self):
        """Build the criterion from the information the user entered."""

        criterion = DefaultCriterion(self.component_manager)
        for hbox in self.tags_box.get_children():
            children = hbox.get_children()
            if children[0].get_active():
                label = children[1].get_label()
                tag_name = unicode( \
                    re.search(r'(.+) \(\d+ cards\)', label).group(1))
                criterion.active_tag__ids.add(self.tags_dict[tag_name])
        return criterion

    def back_to_main_menu_cb(self, widget):
        """Returns to main menu."""

        self.main_widget().switcher.remove_page(self.page)
        self.main_widget().menu_('importcards')

    def ok_button_cb(self, widget):
        """Ok """

        from mnemosyne.libmnemosyne.file_formats.tsv import import_txt_2
        self.component_manager.get_current("file_format").do_import("./test_import/anki.txt") 
