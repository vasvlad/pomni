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
Hildon UI: Input mode Widgets.
"""

import gettext
import gtk
import gtk.glade

from mnemosyne.libmnemosyne.ui_component import UiComponent

_ = gettext.gettext

class RainbowInputWidget(UiComponent):
    
    menu, review = 0, 1

    def __init__(self, component_manager):
        UiComponent.__init__(self, component_manager)

        self.w_tree = self.main_widget().w_tree
        self.switcher = self.main_widget().switcher

        signals = ["add_card", "change_card_type", "input_to_main_menu"]
        self.w_tree.signal_autoconnect(\
             dict([(sig, getattr(self, sig + "_cb")) for sig in signals]))
        
        self.cardtypes_widget = self.w_tree.get_widget('cardtypes')
        self.categories = self.w_tree.get_widget("categories")
        self.categories_liststore = gtk.ListStore(str)
        self.categories.set_model(self.categories_liststore)
        self.categories.set_text_column(0)
        self.init_listboxes()
        #self.layout()

        # Turn off hildon autocapitalization
        try:
            for widget in ("question_box_text", "answer_box_text",
                           "pronun_box_text"):
                self.w_tree.get_widget(widget).\
                    set_property("hildon-input-mode", 'full')
        except (TypeError, AttributeError): # stock gtk doesn't have hildon properties
            pass # so, skip silently


    # callbacks
    def input_to_main_menu_cb(self, widget):
        """Return to main menu."""

        self.switcher.set_current_page(self.menu)


    def add_card_cb(self, widget):
        """ Add card to database. """

        try:
            fact_data = self.get_widgets_data()
        except ValueError:
            return # Let the user try again to fill out the missing data.

        # Create new card
        self.ui_controller_main().create_new_cards(fact_data, 
            self.card_type, -1, [\
            self.categories.get_child().get_text()], True)
        self.database().save(self.config()['path'])

        # clear widgets
        for widget in ("question_box_text", "answer_box_text",
                        "pronun_box_text"):
            self.w_tree.get_widget(widget).get_buffer().set_text("")


    def change_card_type_cb(self, widget):
        """ Changes cardtype when user choose it from listbox. """

        # set card types
        cardtypes = dict([(card_type.id, card_type) \
            for card_type in self.card_types()])
       
        selected_id = int(self.cardtypes_widget.get_active())
        if selected_id == -1:
            selected_id = 0
        selected_id += 1
        self.card_type = cardtypes.get(str(selected_id))

        # show prononsiation if needed
        self.w_tree.get_widget("pronun_box").set_property('visible',
            self.card_type.id == '3')


    # other methods
    def get_widgets_data(self, check_for_required=True):
        """ Get data from widgets. """

        fact = {}
        question_widget = self.w_tree.get_widget("question_box_text")
        answer_widget = self.w_tree.get_widget("answer_box_text")
        pronunciation_widget = self.w_tree.get_widget("pronun_box_text")
        if self.card_type.id == '3':
            widgets = [('f', question_widget), ('t', answer_widget), \
                ('p', pronunciation_widget)]
        else:
            widgets = [('q', question_widget), ('a', answer_widget)]
        for fact_key, widget in widgets:
            start, end = widget.get_buffer().get_bounds()
            fact[fact_key] = widget.get_buffer().get_text(start, end)

        if check_for_required:
            for required in self.card_type.required_fields():
                if not fact[required]:
                    raise ValueError
        return fact


    def init_listboxes(self):
        """ Fill listboxes by categories and cardtypes. """
    
        # Fill Categories list
        self.update_categories()

        # Fill Card-types list
        cardtypes = dict([(card_type.id, card_type) \
            for card_type in self.card_types()])
        cardtypes_liststore = gtk.ListStore(str)
        for key in sorted(cardtypes.keys()):
            cardtypes_liststore.append([cardtypes.get(key).name])
        self.cardtypes_widget.set_model(cardtypes_liststore)
        self.cardtypes_widget.set_text_column(0)
        if cardtypes:
            self.cardtypes_widget.get_child().set_text(\
                cardtypes.get(sorted(cardtypes.keys())[0]).name)
        self.card_type = cardtypes.get(sorted(cardtypes.keys())[0])


    def get_data(self, check_for_required=True):
        """ Get data from widgets. """

        fact = {}
        for edit_box, fact_key in self.edit_boxes.iteritems():
            start, end = edit_box.get_buffer().get_bounds()
            fact[fact_key] = edit_box.get_buffer().get_text(start, end)

        if not check_for_required:
            return fact
        for required in self.card_type.required_fields():
            if not fact[required]:
                raise ValueError
        return fact

    def update_categories(self):
        """ Update categories listbox content. """

        self.categories_liststore.clear()
        categories = dict([(i, name) for (i, name) in \
            enumerate(self.database().tag_names())])
        if categories.values():
            for category in sorted(categories.values()):
                self.categories_liststore.append([category])
            # self.categories - categories listbox
            self.categories.get_child().set_text(\
                sorted(categories.values())[0])
        else:
            self.categories.get_child().set_text("default category")


    def activate(self, fact = None):
        """Activate input mode."""

        self.update_categories()


# Local Variables:
# mode: python
# py-indent-offset: 4
# indent-tabs-mode nil
# tab-width 4
# End:
