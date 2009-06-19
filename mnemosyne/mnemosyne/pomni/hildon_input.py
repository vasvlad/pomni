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
import os


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



class RainbowControllerInput(HildonUiControllerInput):
    """ Rainbow Input mode controller """

    def __init__(self, w_tree):
        """ Initialization items of input window. """

        signals = ["add_card", "input_to_main_menu", "change_card_type",
            "add_picture", "select_item", "close_image_selection_dialog",
            "change_category", "create_new_category", "clear_text",
            "show_add_category_block", "hide_add_category_block"]
        HildonUiControllerInput.__init__(self, w_tree, signals)
        self.update = None
        self.cardtypes = {}
        self.categories_list = []
        self.images_liststore = gtk.ListStore(str, gtk.gdk.Pixbuf)
        self.iconview_widget.set_model(self.images_liststore)
        self.iconview_widget.set_pixbuf_column(1)
        self.set_card_type()
        self.layout()

        # Turn off hildon autocapitalization
        try:
            for widget in (self.question_text_w, self.answer_text_w,
                           self.pronun_text_w, self.foreign_text_w,
                           self.translation_text_w, self.cloze_text_w):
                widget.set_property("hildon-input-mode", 'full')
        except (TypeError, AttributeError): # stock gtk doesn't have hildon properties
            pass # so, skip silently

    def activate(self, fact = None):
        """ Start input window. """
        
        self.fact = fact
        self.update = fact is not None

        self.update_categories()
        self.clear_widgets()
        if fact: # If enter from Review mode
            self.card_type = fact.card_type
            self.layout()
            self.set_widgets_data(fact)
        
        self.switcher.set_current_page(self.input)

    def layout (self):
        """ Switches to neccessary input page. It depends on card_type. """

        if self.card_type:        
            cardtype_dict = {
                _("Front-to-back only"): 0,
                _("Front-to-back and back-to-front"): 0, 
                _("Foreign word with pronunciation"): 1,
                _("Cloze deletion"): 2 }
            self.card_type_switcher_w.set_current_page(\
                cardtype_dict[self.card_type.name])

    def set_card_type(self):
        """ Set current card type. """

        if not self.cardtypes:
            self.cardtypes = dict([(card_type.id, card_type) \
                for card_type in card_types()])
        widgets_cardtypes_dict = {
        "front_to_back_mode_selector_w": _("Front-to-back only"),\
        "both_way_mode_selector_w": _("Front-to-back and back-to-front"),\
        "three_side_mode_selector_w": _("Foreign word with pronunciation"),\
        "cloze_mode_selector_w": _("Cloze deletion")}
        for widget_name, cardtype_name in widgets_cardtypes_dict.items():
            widget = self.w_tree.get_widget(widget_name)
            if widget.get_active() == True:
                for cardtype in self.cardtypes.values():
                    if cardtype.name == cardtype_name:
                        self.card_type = cardtype
                        return

    def update_categories(self):
        """ Update categories list content. """

        self.categories_list = []
        categories = dict([(i, name) for (i, name) in \
            enumerate(database().category_names())])
        if categories.values():
            for category in sorted(categories.values()):
                self.categories_list.append(category)
            self.category_name_w.set_text(sorted(categories.values())[0])
        else:
            self.categories_list.append("default category")
            self.category_name_w.set_text("default category")

    def get_widgets_data(self, check_for_required=True):
        """ Get data from widgets. """

        fact = {}
        if self.card_type.name == _("Foreign word with pronunciation"):
            widgets = [('f', self.foreign_text_w), 
                       ('t', self.translation_text_w), 
                       ('p', self.pronun_text_w)]
        elif self.card_type.name ==  _("Cloze deletion"):
            widgets = [('text', self.cloze_text_w)]
        else:
            widgets = [('q', self.question_text_w),
                       ('a', self.answer_text_w)]
        for fact_key, widget in widgets:
            start, end = widget.get_buffer().get_bounds()
            fact[fact_key] = widget.get_buffer().get_text(start, end)

        if check_for_required:
            for required in self.card_type.required_fields():
                if not fact[required]:
                    raise ValueError
        return fact

    def set_widgets_data(self, fact):
        """ Set widgets data from fact. """

        if self.card_type.name == _("Foreign word with pronunciation"):
            widgets = [('f', self.foreign_text_w),
                       ('t', self.translation_text_w),
                       ('p', self.pronun_text_w)]
        elif self.card_type.name ==  _("Cloze deletion"):
            widgets = [('text', cloze_text_w)]
        else:
            widgets = [('q', self.question_text_w),
                       ('a', self.answer_text_w)]
        for fact_key, widget in widgets:
            widget.get_buffer().set_text(fact[fact_key])

    def clear_widgets(self):
        """ Clear data in widgets. """

        self.question_text_w.get_buffer().set_text("Type QUESTION here...")
        self.answer_text_w.get_buffer().set_text("Type ANSWER here...")
        self.foreign_text_w.get_buffer().set_text("Type FOREIGN here...")
        self.pronun_text_w.get_buffer().set_text("Type PRONUNCIATION here...")
        self.translation_text_w.get_buffer().set_text("Type TRANSLATION here...")
        self.cloze_text_w.get_buffer().set_text("Type TEXT here...")

    def change_card_type_cb(self, widget):
        """ Changes cardtype when user choose it from cardtype column. """

        self.clear_widgets()
        self.set_card_type()
        self.layout()

    def add_card_cb(self, widget):
        """ Add card to database. """

        try:
            fact_data = self.get_widgets_data()
        except ValueError:
            return # Let the user try again to fill out the missing data.

        main = ui_controller_main()
        if self.update: #Update card
            main.update_related_cards(self.fact, fact_data, self.card_type,\
                [self.category_name_w.get_text()], None)
        else: #Create new card
            main.create_new_cards(fact_data, self.card_type, 0, [\
                self.category_name_w.get_text()], True)
                
        self.clear_widgets()
        if self.update:
            self.switcher.set_current_page(self.review)

    def change_category_cb(self, widget):
        """ Change current category. """

        if widget.name == "prev_category_w":
            direction = -1
        direction = 1
        category_index = self.categories_list.index(\
            self.category_name_w.get_text())
        try:
            new_category = self.categories_list[category_index + direction]
        except IndexError:
            if direction:
                new_category = self.categories_list[0]
            else:
                new_category = self.categories_list[len(self.categories_list)-1]
        self.category_name_w.set_text(new_category)

    def create_new_category_cb(self, widget):
        """ Create new category. """
        
        new_category = self.input_mode_new_category_entry.get_text()
        if new_category:
            self.categories_list.append(new_category)
            self.input_mode_new_category_entry.set_text("")
            self.hide_add_category_block_cb(None)

    def add_picture_cb(self, widget):
        """ Show image selection dialog. """

        def resize_image(pixbuf):
            x_ratio = pixbuf.get_width() / 64.0
            y_ratio = pixbuf.get_height() / 64.0
            new_width = int(pixbuf.get_width() / x_ratio)
            new_height = int(pixbuf.get_height() / y_ratio)
            return pixbuf.scale_simple(\
                new_width, new_height, gtk.gdk.INTERP_BILINEAR)

        self.images_liststore.clear()
        self.imagedir = config()['imagedir']
        if not os.path.exists(self.imagedir):
            self.imagedir = "./images" # on Desktop
            if not os.path.exists(self.imagedir):
                ui_controller_main().widget.information_box(\
                    _("'Images' directory does not exist!"), "OK")
                return                
        if os.listdir(self.imagedir):
            self.image_selection_dialog.show()
            for file in os.listdir(self.imagedir):
                if os.path.isfile(os.path.join(self.imagedir, file)):
                    pixbuf = gtk.gdk.pixbuf_new_from_file(\
                        os.path.join(self.imagedir, file))
                    self.images_liststore.append([file, resize_image(pixbuf)])
            #self.image_selection_dialog.show()
        else:
            ui_controller_main().widget.information_box(\
                _("There are no files in 'Images' directory!"), "OK")
            
    def select_item_cb(self, widget):
        """ 
        Set html-text with image path when user
        select image from image selection dialog. 
        """

        self.image_selection_dialog.hide()
        item_index = self.iconview_widget.get_selected_items()[0]
        item_text = self.images_liststore.get_value(\
            self.images_liststore.get_iter(item_index),0)
        self.question_text_w.get_buffer().set_text(\
            "<img src='%s'>" % os.path.join(self.imagedir, item_text))
      
    def close_image_selection_dialog_cb(self, widget):
        """ Close image selection dialog. """

        self.image_selection_dialog.hide()

    def clear_text_cb(self, widget, event):
        """ Clear textview content. """

        widget.get_buffer().set_text("")

    def show_add_category_block_cb(self, widget):
        """ Shows add category block. """

        self.input_mode_change_category_block.hide()
        self.input_mode_add_category_block.show()
        self.input_mode_new_category_entry.grab_focus()

    def hide_add_category_block_cb(self, widget):
        """ Hides add category block. """

        self.input_mode_change_category_block.show()
        self.input_mode_add_category_block.hide()

    def input_to_main_menu_cb(self, widget):
        """ Return to main menu. """

        self.switcher.set_current_page(self.main_menu)


# Local Variables:
# mode: python
# py-indent-offset: 4
# indent-tabs-mode nil
# tab-width 4
# End:
