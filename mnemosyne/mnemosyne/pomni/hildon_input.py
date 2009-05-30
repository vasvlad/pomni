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
# pomni

"""
Hildon UI: Input mode classes.
"""

import gettext
import gtk
import gtk.glade


from mnemosyne.libmnemosyne.component_manager import database, config, \
        ui_controller_main, card_types
from pomni.hildon_ui import HildonBaseController
_ = gettext.gettext


class HildonUiControllerInput(HildonBaseController):
    """ Hildon Input controller """

    def __init__(self, w_tree, signals):
        """ Initialization items of input window. """

        HildonBaseController.__init__(self, w_tree)
        self.w_tree.signal_autoconnect(\
            dict([(sig, getattr(self, sig + "_cb")) for sig in signals]))


class EternalControllerInput(HildonUiControllerInput):
    """ Eternal Input mode controller """

    def __init__(self, w_tree):
        """ Initialization items of input window. """

        signals = ["add_card", "add_card2", "input_to_main_menu"]
        HildonUiControllerInput.__init__(self, w_tree, signals)

        self.fields_container = None
        self.liststore = None
        self.card_type = None
        self.fact = None
        self.update = None
        self.edit_boxes = {}

    def create_entries (self, fact = None):
        """ Create widget inclusive varios entries. """

        fields_container = gtk.VBox()
        fields_container.set_name('fields_container')
        fields_container.show()
        for fact_key, fact_key_name in self.card_type.fields:
            # Top Alignment
            aligment = gtk.Alignment()
            aligment.set_property("height-request", 100)
            fields_container.pack_start(aligment, True, True, 0)
            # Label of field
            labelbox = gtk.HBox()
            left_aligment_of_label = gtk.Alignment()
            left_aligment_of_label.set_property("width-request", 10)
            left_aligment_of_label.show()
            name_field = gtk.Label(fact_key_name)
            labelbox.pack_start(left_aligment_of_label, False, False, 0)
            labelbox.pack_start(name_field, False, False, 0)
            labelbox.pack_start(gtk.Alignment(), True, True, 0)
            name_field.show()
            labelbox.show()
            fields_container.pack_start(labelbox, True, True, 0)
            # Entry
            framebox = gtk.HBox()
            #Left Alignment
            left_aligment_of_frame = gtk.Alignment()
            left_aligment_of_frame.set_property("width-request", 10)
            left_aligment_of_frame.show()
            framebox.pack_start(left_aligment_of_frame, False, False, 0)
            #TextView itself
            surface = gtk.Notebook()
            surface.set_property('show_tabs', False)
            surface.set_name('question_frame')
            entry_field = gtk.TextView()
            #Fill entry
            if fact:
                textbuffer = entry_field.get_buffer()
                textbuffer.set_text(fact.data[fact_key])
            entry_field.set_property("height-request", 120)
            entry_field.set_name(fact_key_name)
            entry_field.show()
            self.edit_boxes[entry_field] = fact_key
            surface.append_page(entry_field)
            framebox.pack_start(surface, True, True, 0)
            surface.show()
            #Right Alignment
            right_aligment_of_frame = gtk.Alignment()
            right_aligment_of_frame.set_property("width-request", 10)
            framebox.pack_start(right_aligment_of_frame, False, False, 0)
            right_aligment_of_frame.show()
            framebox.show()

            fields_container.pack_start(framebox, True, True, 0)

        return fields_container

    def activate(self, fact = None):
        """ Start input window. """

        self.fact = fact
        self.update = fact is not None

        card_type_by_id = dict([(card_type.id, card_type) \
            for card_type in card_types()])

        #FIX ME for all types of card 
        #Now default card type 1 (Front-to-back only) 
        self.card_type = card_type_by_id.get('1')

        #Destroy container if it was created early
        if self.fields_container:
            self.fields_container.destroy()

        #Prepare fields_container
        parent_fields_container = \
                               self.w_tree.get_widget('fields_container_parent')
        self.fields_container = self.create_entries(self.fact)
        parent_fields_container.pack_start(self.fields_container, True, True, 0)

        category_names_by_id = dict([(i, name) for (i, name) in \
            enumerate(database().category_names())])

        # switch to Page Input
        self.switcher.set_current_page(self.input)

        categories = self.w_tree.get_widget("categories")
        self.liststore = gtk.ListStore(str)

        self.liststore.clear()
        for category in category_names_by_id.values():
            self.liststore.append([category])
        categories.set_model(self.liststore)
        categories.set_text_column(0)
        if category_names_by_id.values():
            categories.get_child().set_text(category_names_by_id.values()[0])


    def add_card_cb(self, widget):
        """ Add card to database. """

        try:
            fact_data = self.get_data()
        except ValueError:
            return # Let the user try again to fill out the missing data.

        main = ui_controller_main()

        if self.update:
            # Update card
            main.update_related_cards(self.fact, fact_data,
                                    self.card_type,
                                    [self.categories.get_child().get_text()],
                                    None)
        else:
            # Create new card
            main.create_new_cards(fact_data, self.card_type, 5,
                [self.categories.get_child().get_text()])

        database().save(config()['path'])

        #FIX ME need checking for success for previous operations
        self.clear_data_widgets()

        if self.update:
            self.switcher.set_current_page(self.review)


    def add_card2_cb(self, widget, event):
        """ Hook for add_card for eventboxes. """

        self.add_card_cb (widget)


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


    def clear_data_widgets(self):
        """ Clear data in widgets. """

        self.edit_boxes = {}

        #FIX ME It may work more faster if I make clearing only edit_box

        #Destroy fields_container 
        if self.fields_container:
            self.fields_container.destroy()

        #Prepare fields_container
        parent_fields_container = \
            self.w_tree.get_widget('fields_container_parent')
        self.fields_container = self.create_entries()
        parent_fields_container.pack_start(self.fields_container, 
            True, True, 0)

    def input_to_main_menu_cb(self, widget):
        """ Return to main menu. """

        #Destroy fields_container
        if self.fields_container:
            self.fields_container.destroy()
        self.switcher.set_current_page(self.main_menu)
        #Destroy categories entry
#        if self.listsore:
#            self.liststore.destroy()



class RainbowControllerInput(HildonUiControllerInput):
    """ Rainbow Input mode controller """

    def __init__(self, w_tree):
        """ Initialization items of input window. """

        signals = ["add_card", "change_card_type", "input_to_main_menu"]
        HildonUiControllerInput.__init__(self, w_tree, signals)
        self.fill_listboxes()
        self.layout()

    def layout (self):
        """ Hides or shows neccessary widgets. It depends on card_type. """

        if self.card_type:        
            self.pronun_box.set_property('visible', self.card_type.id == '3')

    def set_card_type(self):
        """ Set card type when user select it in cardtypes listbox. """

        cardtypes = dict([(card_type.id, card_type) \
            for card_type in card_types()])
        selected_id = (int(self.cardtypes.get_active()) + 1).__str__()
        self.card_type = cardtypes.get(selected_id)

    def change_card_type_cb(self, widget):
        """ Changes cardtype when user choose it from listbox. """

        self.set_card_type()
        self.layout()


    def fill_listboxes(self):
        """ Fill listboxes by categories and cardtypes. """

        # Fill Categories list
        # categories = { id:category, ...}
        categories = dict([(i, name) for (i, name) in \
            enumerate(database().category_names())])
        categories_widget = self.categories
        categories_liststore = gtk.ListStore(str)
        for category in sorted(categories.values()):
            categories_liststore.append([category])
        categories_widget.set_model(categories_liststore)
        categories_widget.set_text_column(0)
        if categories.values():
            categories_widget.get_child().set_text(\
                sorted(categories.values())[0])
        else:
            categories_widget.get_child().set_text("default category")
        
        # Fill Card-types list
        # cardtypes = { id:card_type_object, ...}
        cardtypes = dict([(card_type.id, card_type) \
            for card_type in card_types()])
        cardtypes_widget = self.cardtypes
        cardtypes_liststore = gtk.ListStore(str)
        for key in sorted(cardtypes.keys()):
            cardtypes_liststore.append([cardtypes.get(key).name])
        cardtypes_widget.set_model(cardtypes_liststore)
        cardtypes_widget.set_text_column(0)
        if cardtypes:
            cardtypes_widget.get_child().set_text(\
                cardtypes.get(sorted(cardtypes.keys())[0]).name)
        self.card_type = cardtypes.get(sorted(cardtypes.keys())[0])

    def activate(self, fact = None):
        """ Start input window. """

        self.switcher.set_current_page(self.input)

    def add_card_cb(self, widget):
        """ Add card to database. """

        try:
            fact_data = self.get_widgets_data()
        except ValueError:
            return # Let the user try again to fill out the missing data.

        # Create new card
        card = ui_controller_main()
        card.create_new_cards(fact_data, self.card_type, 0, [\
            self.categories.get_child().get_text()], True)
        database().save(config()['path'])
        self.clear_widgets()

    def get_widgets_data(self, check_for_required=True):
        """ Get data from widgets. """

        fact = {}
        question_widget = self.question_box_text
        answer_widget = self.answer_box_text
        pronunciation_widget = self.pronun_box_text
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

    def clear_widgets(self):
        """ Clear data in widgets. """

        self.question_box_text.get_buffer().set_text("")
        self.answer_box_text.get_buffer().set_text("")
        self.pronun_box_text.get_buffer().set_text("")

    def input_to_main_menu_cb(self, widget):
        """ Return to main menu. """

        self.switcher.set_current_page(self.main_menu)


# Local Variables:
# mode: python
# py-indent-offset: 4
# indent-tabs-mode nil
# tab-width 4
# End:
