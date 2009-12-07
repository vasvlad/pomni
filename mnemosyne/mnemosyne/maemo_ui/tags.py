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
Hildon UI: Tags widget.
"""

import mnemosyne.maemo_ui.widgets.tags as widgets

from mnemosyne.libmnemosyne.ui_components.dialogs import ActivateCardsDialog
from mnemosyne.libmnemosyne.activity_criteria.default_criterion import \
    DefaultCriterion


class NonBlockingActivateCardsDialog(ActivateCardsDialog):
    """Non blocking variant of ActivateCardsDialog."""

    def activate_cards(self):
        """This part is the first part of activate_cards
           from default controller."""

        self.stopwatch().pause()
        self.component_manager.get_current("activate_cards_dialog") \
            (self.component_manager).activate()

    def update_ui(self, review_controller):
        """This part is called from tags_to_main_menu_cb,
           when tags is selected."""

        review_controller.reset_but_try_to_keep_current_card()
        review_controller.reload_counters()
        review_controller.update_status_bar()
        self.stopwatch().unpause()


class TagsWidget(NonBlockingActivateCardsDialog):
    """Activate cards widget."""
    
    def __init__(self, component_manager):
        NonBlockingActivateCardsDialog.__init__(self, component_manager)
        self.page, self.tags_box, menu_button = widgets.create_tags_ui( \
            self.main_widget().switcher)
        self.tags_dict = {}
        # connecting signals
        menu_button.connect('clicked', self.tags_to_main_menu_cb)

    def activate(self):
        """Activate 'ActivateCardsDialog'."""

        self.main_widget().switcher.set_current_page(self.page)
        self.display_criterion(self.database().current_activity_criterion())

    def display_criterion(self, criterion):
        """Display current criterion."""

        tags_box = self.tags_box
        for child in tags_box.get_children():
            tags_box.remove(child)
        for tag in self.database().get_tags():
            self.tags_dict[tag.name] = tag._id
            tags_box.pack_start(widgets.create_tag_checkbox( \
                tag.name, tag._id in criterion.active_tag__ids))

    def get_criterion(self):
        """Build the criterion from the information the user entered."""

        criterion = DefaultCriterion(self.component_manager)
        for hbox in self.tags_box.get_children():
            children = hbox.get_children()
            if children[0].get_active():
                criterion.active_tag__ids.add(\
                    self.tags_dict[unicode(children[1].get_label())])
        return criterion

    def tags_to_main_menu_cb(self, widget):
        """Return to main menu."""

        self.database().set_current_activity_criterion(self.get_criterion())
        self.update_ui(self.review_controller())
        self.main_widget().switcher.remove_page(self.page)
        self.main_widget().menu_()
