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
import os

from mnemosyne.libmnemosyne.ui_components.dialogs import AddCardsDialog
from mnemosyne.libmnemosyne.card_types.front_to_back import FrontToBack
from mnemosyne.libmnemosyne.card_types.both_ways import BothWays
from mnemosyne.libmnemosyne.card_types.three_sided import ThreeSided
from mnemosyne.libmnemosyne.card_types.cloze import Cloze

_ = gettext.gettext

class RainbowInputWidget(AddCardsDialog):
    """Input mode widget for Rainbow theme."""
    
    def __init__(self, component_manager):
        AddCardsDialog.__init__(self, component_manager)

        self.w_tree = self.main_widget().w_tree

        signals = ["add_card", "input_to_main_menu", "change_card_type",
            "add_picture", "select_item", "close_media_selection_dialog",
            "change_category", "create_new_category", "clear_text",
            "add_sound", "show_add_category_block", 
            "hide_add_category_block", "preview_sound_in_input"]

        self.w_tree.signal_autoconnect(\
             dict([(sig, getattr(self, sig + "_cb")) for sig in signals]))
        
        self.fact = None
        self.update = None
        self.sounddir = None
        self.imagedir = None
        self.card_type = None
        self.categories_list = []
        #liststore = [text, type, filename, dirname, pixbuf]
        self.liststore = gtk.ListStore(str, str, str, str, gtk.gdk.Pixbuf)
        iconview_widget = self.w_tree.get_widget("iconview_widget")
        iconview_widget.set_model(self.liststore)
        iconview_widget.set_pixbuf_column(4)
        iconview_widget.set_text_column(0)

        # Widgets as attributes
        self.areas = {# Text areas
            "cloze": self.w_tree.get_widget("cloze_text_w"),
            "answer":  self.w_tree.get_widget("answer_text_w"),
            "foreign": self.w_tree.get_widget("foreign_text_w"),
            "question": self.w_tree.get_widget("question_text_w"),
            "translation": self.w_tree.get_widget("translation_text_w"),
            "pronunciation": self.w_tree.get_widget("pronun_text_w")
        }
        self.widgets = {# Other widgets
            "CurrentCategory": self.w_tree.get_widget("category_name_w"),
            "SoundButton": self.w_tree.get_widget("sound_content_button"),
            "PictureButton": self.w_tree.get_widget("picture_content_button"),
            "SoundIndicator": self.w_tree.get_widget("input_mode_snd_button"),
            "CardTypeSwithcer": self.w_tree.get_widget("card_type_switcher_w"),
            "MediaDialog": self.w_tree.get_widget("media_selection_dialog"),
            "SoundContainer": self.w_tree.get_widget(\
                "input_mode_snd_container"),
            "QuestionContainer": self.w_tree.get_widget(\
                "input_mode_question_container"),
            "NewCategory": self.w_tree.get_widget(\
                "input_mode_new_category_entry"),
            "ChangeCategoryBlock": self.w_tree.get_widget(\
                "input_mode_change_category_block"),
            "AddCategoryBlock": self.w_tree.get_widget(\
                "input_mode_add_category_block")
        }
        # card_id: {"page": page_id, "selector": selector_widget, 
        # "widgets": [(field_name:text_area_widget)...]}
        self.selectors = {
            FrontToBack.id: {
            "page": 0, 
            "selector": self.w_tree.get_widget("front_to_back_mode_selector_w"),
            "widgets": [('q', self.areas["question"]), 
                        ('a', self.areas["answer"])]
            },
            BothWays.id: {
            "page": 0,
            "selector": self.w_tree.get_widget("both_way_mode_selector_w"),
            "widgets": [('q', self.areas["question"]), 
                        ('a', self.areas["answer"])]
            },
            ThreeSided.id: {
            "page": 1,
            "selector": self.w_tree.get_widget("three_side_mode_selector_w"),
            "widgets": [('f', self.areas["foreign"]),
                        ('t', self.areas["translation"]),
                        ('p', self.areas["pronunciation"])]
            },
            Cloze.id: {
            "page": 2,
            "selector": self.w_tree.get_widget("cloze_mode_selector_w"),
            "widgets": [('text', self.areas["cloze"])]
            }
        }
        # add card_type to selectors subdict
        for card_type in self.card_types():
            self.selectors[card_type.id]["card_type"] = card_type

        # create {selector_widget:card_type.id} dict
        self.widget_card_id = dict((self.selectors[id]["selector"], id) \
            for id in self.selectors.keys())

        self.set_card_type(self.w_tree.get_widget( \
            "front_to_back_mode_selector_w"))
        self.compose_widgets()

        # Turn off hildon autocapitalization
        try:
            for widget in self.areas.values():
                widget.set_property("hildon-input-mode", 'full')
        # stock gtk doesn't have hildon properties
        except (TypeError, AttributeError): 
            pass # so, skip silently

    def activate(self, fact=None):
        """Activate input mode."""

        self.stop_playing()
        self.fact = fact
        self.update = fact is not None
        
        self.update_categories()
        self.clear_widgets()
        if fact: # If enter from Review mode
            self.card_type = fact.card_type
            self.compose_widgets()
            self.set_widgets_data(fact)

        self.show_snd_container()

    def show_snd_container(self):
        """ Shows or hides snd container. """
                    
        start, end = self.areas["question"].get_buffer().get_bounds()
        text = self.areas["question"].get_buffer().get_text(start, end)
        if "sound src=" in text:
            self.widgets["QuestionContainer"].hide()
            self.widgets["SoundContainer"].show()
        else:
            self.widgets["QuestionContainer"].show()
            self.widgets["SoundContainer"].hide()

    def compose_widgets (self):
        """Switches to neccessary input page. It depends on card_type."""

        self.widgets["CardTypeSwithcer"].set_current_page( \
            self.selectors[self.card_type.id]["page"])
        self.selectors[self.card_type.id]["selector"].set_active(True)
        state = self.card_type.id in (BothWays.id, FrontToBack.id)
        self.widgets["PictureButton"].set_sensitive(state)
        self.widgets["SoundButton"].set_sensitive(state)

    def set_card_type(self, widget):
        """Set current card type."""

        card_type_id = self.widget_card_id[widget]
        self.card_type = self.selectors[card_type_id]["card_type"]

    def update_categories(self):
        """Update categories list content."""

        if not self.categories_list:
            categories = dict([(i, name) for (i, name) in \
                enumerate(self.database().tag_names())])
            if categories.values():
                for category in sorted(categories.values()):
                    self.categories_list.append(category)
                self.widgets["CurrentCategory"].set_text( \
                    sorted(categories.values())[0])
            else:
                self.categories_list.append("default category")
                self.widgets["CurrentCategory"].set_text("default category")

    def check_complete_input(self):
        """Check for non empty fields."""

        pattern_list = ["Type %s here..." % item for item in ["ANSWER", \
            "QUESTION", "FOREIGN", "PRONUNCIATION", "TRANSLATION", "TEXT"]]
        pattern_list.append("")
        for fact_key, widget in self.selectors[self.card_type.id]["widgets"]:
            start, end = widget.get_buffer().get_bounds()
            if widget.get_buffer().get_text(start, end) in pattern_list:
                return False
        return True

    def change_category_cb(self, widget):
        """Change current category."""

        if widget.name == "prev_category_w":
            direction = -1
        direction = 1
        category_index = self.categories_list.index( \
            self.widgets["CurrentCategory"].get_text())
        try:
            new_category = self.categories_list[category_index + direction]
        except IndexError:
            if direction:
                new_category = self.categories_list[0]
            else:
                new_category = self.categories_list[len(self.categories_list)-1]
        self.widgets["CurrentCategory"].set_text(new_category)

    def create_new_category_cb(self, widget):
        """Create new category."""

        new_category = self.widgets["NewCategory"].get_text()
        if new_category:
            self.categories_list.append(new_category)
            self.widgets["NewCategory"].set_text("")
            self.widgets["CurrentCategory"].set_text(new_category)
            self.hide_add_category_block_cb(None)

    def add_picture_cb(self, widget):
        """Show image selection dialog."""

        def resize_image(pixbuf):
            """Resize image to 64x64 px."""

            x_ratio = pixbuf.get_width() / 64.0
            y_ratio = pixbuf.get_height() / 64.0
            new_width = int(pixbuf.get_width() / x_ratio)
            new_height = int(pixbuf.get_height() / y_ratio)
            return pixbuf.scale_simple(new_width, new_height, \
                gtk.gdk.INTERP_BILINEAR)

        self.main_widget().stop_playing()
        self.liststore.clear()
        self.imagedir = self.config()['imagedir']
        if not os.path.exists(self.imagedir):
            self.imagedir = "./images" # on Desktop
            if not os.path.exists(self.imagedir):
                self.main_widget().information_box(\
                    _("'Images' directory does not exist!"))
                return
        if os.listdir(self.imagedir):
            self.widgets["MediaDialog"].show()
            for fname in os.listdir(self.imagedir):
                if os.path.isfile(os.path.join(self.imagedir, fname)):
                    pixbuf = gtk.gdk.pixbuf_new_from_file(\
                        os.path.join(self.imagedir, fname))
                    self.liststore.append(["", "img", fname, \
                        self.imagedir, resize_image(pixbuf)])
        else:
            self.main_widget().information_box(\
                _("There are no files in 'Images' directory!"))

    def select_item_cb(self, widget):
        """ 
        Set html-text with media path and type when user
        select media filefrom media selection dialog. 
        """

        self.widgets["MediaDialog"].hide()
        item_index = self.w_tree.get_widget("iconview_widget"). \
            get_selected_items()[0]
        item_type = self.liststore.get_value( \
            self.liststore.get_iter(item_index), 1)
        item_fname = self.liststore.get_value( \
            self.liststore.get_iter(item_index), 2)
        item_dirname = self.liststore.get_value( \
            self.liststore.get_iter(item_index), 3)
        question_text = "<%s src='%s'>" % \
            (item_type, os.path.join(item_dirname, item_fname))
        self.areas["question"].get_buffer().set_text(question_text)
        self.show_snd_container()

    def add_sound_cb(self, widget):
        """Show sound selection dialog."""

        self.main_widget().stop_playing()
        self.liststore.clear()
        self.sounddir = self.config()['sounddir']
        if not os.path.exists(self.sounddir):
            self.sounddir = "./sounds" # on Desktop
            if not os.path.exists(self.sounddir):
                self.main_widget().information_box(\
                    _("'Sounds' directory does not exist!"))
                return     
        if os.listdir(self.sounddir):
            self.widgets["MediaDialog"].show()
            for fname in os.listdir(self.sounddir):
                if os.path.isfile(os.path.join(self.sounddir, fname)):
                    sound_logo_file = os.path.join( \
                        self.config()["theme_path"], "soundlogo.png")
                    pixbuf = gtk.gdk.pixbuf_new_from_file(sound_logo_file)
                    self.liststore.append([fname, "sound", fname, \
                        self.sounddir, pixbuf])
        else:
            self.main_widget().information_box(\
                _("There are no files in 'Sounds' directory!"))

    def add_card_cb(self, widget):
        """Add card to database."""

        # check for empty fields
        if not self.check_complete_input():
            return

        try:
            fact_data = self.get_widgets_data()
        except ValueError:
            return # Let the user try again to fill out the missing data.

        main = self.controller()
        if self.update: #Update card
            main.update_related_cards(self.fact, fact_data, self.card_type, \
                [self.widgets["CurrentCategory"].get_text()], None)
            self.main_widget().activate_mode("review")
        else: #Create new card
            main.create_new_cards(fact_data, self.card_type, -1, \
                [self.widgets["CurrentCategory"].get_text()])
            self.clear_widgets()

        self.main_widget().stop_playing()
        self.show_snd_container()

    def get_widgets_data(self, check_for_required=True):
        """ Get data from widgets. """

        fact = {}
        for fact_key, widget in self.selectors[self.card_type.id]["widgets"]:
            start, end = widget.get_buffer().get_bounds()
            fact[fact_key] = widget.get_buffer().get_text(start, end)
        if check_for_required:
            for required in self.card_type.required_fields():
                if not fact[required]:
                    raise ValueError
        return fact

    def set_widgets_data(self, fact):
        """Set widgets data from fact."""

        for fact_key, widget in self.selectors[self.card_type.id]["widgets"]:
            widget.get_buffer().set_text(fact[fact_key])

    def clear_widgets(self):
        """Clear data in widgets."""

        for caption in self.areas.keys():
            self.areas[caption].get_buffer().set_text( \
                "Type %s here..." % caption.upper())

    def change_card_type_cb(self, widget):
        """Changes cardtype when user choose it from cardtype column."""
                
        self.main_widget().stop_playing()
        self.clear_widgets()
        self.show_snd_container()
        self.set_card_type(widget)
        self.compose_widgets()

    def preview_sound_in_input_cb(self, widget):
        """Preview sound in input mode."""

        if widget.get_active():
            start, end = self.areas["question"].get_buffer().get_bounds()
            text = self.areas["question"].get_buffer().get_text(start, end)
            self.main_widget().start_playing(text, self)
        else:
            self.main_widget().stop_playing()

    def update_indicator(self):
        """Set non active state for widget."""

        self.widgets["SoundIndicator"].set_active(False)

    def close_media_selection_dialog_cb(self, widget):
        """Close image selection dialog."""

        self.widgets["MediaDialog"].hide()

    def clear_text_cb(self, widget, event):
        """Clear textview content."""

        if not self.update:
            widget.get_buffer().set_text("")

    def show_add_category_block_cb(self, widget):
        """Shows add category block."""

        self.widgets["ChangeCategoryBlock"].hide()
        self.widgets["AddCategoryBlock"].show()
        self.widgets["NewCategory"].grab_focus()

    def hide_add_category_block_cb(self, widget):
        """Hides add category block."""

        self.widgets["ChangeCategoryBlock"].show()
        self.widgets["AddCategoryBlock"].hide()

    def stop_playing(self):
        """Stop playing audiofile."""

        if self.main_widget().stop_playing():
            self.widgets["SoundIndicator"].set_active(False)

    def input_to_main_menu_cb(self, widget):
        """Return to main menu."""

        self.main_widget().stop_playing()
        self.main_widget().activate_mode("menu")




# Local Variables:
# mode: python
# py-indent-offset: 4
# indent-tabs-mode nil
# tab-width 4
# End:
