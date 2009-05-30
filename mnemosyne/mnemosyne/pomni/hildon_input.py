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

    def __init__(self, w_tree):
        """ Initialization items of input window. """

        HildonBaseController.__init__(self, w_tree)
        signals = ["add_card", "add_card2", "input_to_main_menu"]
        self.w_tree.signal_autoconnect(\
            dict([(sig, getattr(self, sig + "_cb")) for sig in signals]))

        self.fields_container = None
        self.liststore = None
        self.card_type = None
        self.fact = None
        self.update = None
        self.edit_boxes = {}
        self.categories = self.w_tree.get_widget("categories")
        self.liststore = gtk.ListStore(str)
        self.categories.set_model(self.liststore)
        self.categories.set_text_column(0)

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
            # turn off hildon autocapitalization
            try:
                entry_field.set_property("hildon-input-mode", "full")
            except TypeError:
                pass
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

        self.liststore.clear()
        for category in category_names_by_id.values():
            self.liststore.append([category])
        if category_names_by_id.values():
            self.categories.get_child().set_text(category_names_by_id.values()[0])

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


class EternalControllerInput(HildonUiControllerInput):
    """ Eternal Input mode controller """


class RainbowControllerInput(HildonUiControllerInput):
    """ Rainbow Input mode controller """


# Local Variables:
# mode: python
# py-indent-offset: 4
# indent-tabs-mode nil
# tab-width 4
# End:
