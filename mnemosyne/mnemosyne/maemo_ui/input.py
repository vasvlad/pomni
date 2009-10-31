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
Hildon UI: Input mode Widgets.
"""

import os
import gtk
import pango
import gettext

from mnemosyne.maemo_ui.widgets import BaseHildonWidget
from mnemosyne.libmnemosyne.ui_components.dialogs import \
    AddCardsDialog, EditFactDialog
from mnemosyne.libmnemosyne.utils import numeric_string_cmp
from mnemosyne.libmnemosyne.card_types.front_to_back import FrontToBack
from mnemosyne.libmnemosyne.card_types.both_ways import BothWays
from mnemosyne.libmnemosyne.card_types.three_sided import ThreeSided
from mnemosyne.libmnemosyne.card_types.cloze import Cloze
Cloze.required_fields = ["text"]

_ = gettext.gettext

FONT_DISTINCTION = 7

class InputWidget(BaseHildonWidget):
    """Input mode widget for Rainbow theme."""
    
    def __init__(self, component_manager):

        BaseHildonWidget.__init__(self, component_manager)
        get_widget = self.get_widget
        self.connect_signals([\
            ("input_mode_toolbar_button_back_w", "clicked", \
                self.input_to_main_menu_cb),
            ("question_text_w", "button_press_event", \
                self.show_media_dialog_cb),
            ("image_selection_dialog_button_select", "clicked", \
                self.select_item_cb),
            ("iconview_widget", "selection-changed", \
                self.enable_select_button_cb),
            ("image_selection_dialog_button_close", "clicked", \
                self.close_media_selection_dialog_cb),
            ("imput_mode_cardtype_button", "clicked", \
                self.show_cardtype_dialog_cb),
            ("input_mode_content_button", "clicked", \
                self.show_content_dialog_cb),
            ("tags_button", "clicked", self.show_tags_dialog_cb),
            ("new_tag_button", "clicked", self.add_new_tag_cb),
            ("input_mode_snd_button", "released", \
                self.preview_sound_in_input_cb),
            ("front_to_back_cardtype_button", "released", \
                self.set_card_type_cb),
            ("both_ways_cardtype_button", "released", self.set_card_type_cb),
            ("three_sided_cardtype_button", "released", self.set_card_type_cb),
            ("cloze_cardtype_button", "released", self.set_card_type_cb),
            ("text_content_button", "clicked", self.set_content_type_cb),
            ("image_content_button", "clicked", self.set_content_type_cb),
            ("sound_content_button", "clicked", self.set_content_type_cb)])

        self.content_type = None
        self.last_input_page = None
        self.fact = None
        self.tag_mode = False
        self.sounddir = None
        self.imagedir = None
        self.card_type = None
        self.selected_tags = None
        self.tags = sorted(self.database().get_tag_names(), \
            cmp=numeric_string_cmp) or [_("<default>")]
        self.added_new_cards = False
        #liststore = [text, type, filename, dirname, pixbuf]
        self.liststore = gtk.ListStore(str, str, str, str, gtk.gdk.Pixbuf)
        iconview_widget = get_widget("iconview_widget")
        iconview_widget.set_model(self.liststore)
        iconview_widget.set_pixbuf_column(4)
        iconview_widget.set_text_column(0)

        # Widgets as attributes
        self.areas = {# Text areas
            "cloze": get_widget("cloze_text_w"),
            "answer":  get_widget("answer_text_w"),
            "foreign": get_widget("foreign_text_w"),
            "question": get_widget("question_text_w"),
            "translation": get_widget("translation_text_w"),
            "pronunciation": get_widget("pronun_text_w")
        }

        # Change default font
        font = pango.FontDescription("Nokia Sans %s" % \
            (self.conf['font_size'] - FONT_DISTINCTION))
        for area in self.areas.values():
            area.modify_font(font)

        self.widgets = {# Other widgets
            "CardTypeButton": get_widget("imput_mode_cardtype_button"),
            "ContentButton": get_widget("input_mode_content_button"),
            "CardTypeSwitcher": get_widget("card_type_switcher_w"),
            "AddCardButton":get_widget("input_mode_toolbar_add_card_w"),
            "SoundContainer": get_widget("input_mode_snd_container"),
            "QuestionContainer": get_widget("input_mode_question_container")
        }

        # card_id: {"page": page_id, "selector": selector_widget, 
        # "widgets": [(field_name:text_area_widget)...]}
        self.selectors = {
            FrontToBack.id: {
            "page": 0, 
            "selector": get_widget("front_to_back_cardtype_button"),
            "widgets": [('q', self.areas["question"]), 
                        ('a', self.areas["answer"])]
            },
            BothWays.id: {
            "page": 0,
            "selector": get_widget("both_ways_cardtype_button"),
            "widgets": [('q', self.areas["question"]), 
                        ('a', self.areas["answer"])]
            },
            ThreeSided.id: {
            "page": 1,
            "selector": get_widget("three_sided_cardtype_button"),
            "widgets": [('f', self.areas["foreign"]),
                        ('t', self.areas["translation"]),
                        ('p', self.areas["pronunciation"])]
            },
            Cloze.id: {
            "page": 2,
            "selector": get_widget("cloze_cardtype_button"),
            "widgets": [('text', self.areas["cloze"])]
            }
        }
        # add card_type to selectors subdict
        for card_type in self.card_types():
            self.selectors[card_type.id]["card_type"] = card_type

        # Turn off hildon autocapitalization
        try:
            for widget in self.areas.values():
                widget.set_property("hildon-input-mode", 'full')
        # stock gtk doesn't have hildon properties
        except (TypeError, AttributeError): 
            pass # so, skip silently

    def show_snd_container(self):
        """Show or hide PlaySound button. """
                    
        start, end = self.areas["question"].get_buffer().get_bounds()
        text = self.areas["question"].get_buffer().get_text(start, end)
        if "sound src=" in text:
            self.widgets["QuestionContainer"].hide()
            self.widgets["SoundContainer"].show()
        else:
            self.widgets["QuestionContainer"].show()
            self.widgets["SoundContainer"].hide()

    def set_card_type(self, card_type):
        """Set current Card type value and changes UI."""

        self.card_type = card_type
        # This trick need for set right image for CardType button from rcfile
        self.widgets["CardTypeButton"].set_name("cardtype_%s" % card_type.id)
        self.widgets["CardTypeSwitcher"].set_current_page( \
            self.selectors[card_type.id]["page"])

    def set_content_type(self, widget_name):
        """Set current Content type and changes UI."""

        self.content_type = widget_name.split('_')[0]
        # This trick need for set right image for ContentType button from rcfile
        self.widgets["ContentButton"].set_name( \
            "contenttype_%s" % self.content_type)

    def update_tags(self):
        """Update active tags list."""

        selected_tags = [tag.strip() for tag in self.selected_tags.split(',') \
            if tag.strip() in self.tags]
        self.get_widget("tags_button").set_label( \
            ", ".join(selected_tags) or _("<default>"))

    def check_complete_input(self):
        """Check for non empty fields."""

        pattern_list = [item for item in [_("<ANSWER>"), _("<QUESTION>"), \
            _("<FOREIGN>"), _("<PRONUNCIATION>"), _("<TRANSLATION>"), \
            _("<TEXT>"), ""]]
        for selector in self.selectors[self.card_type.id]["widgets"]:
            buf = selector[1].get_buffer()
            start, end = buf.get_bounds()
            if buf.get_text(start, end) in pattern_list:
                return False
        return True

    def get_widgets_data(self, check_for_required=True):
        """Get data from widgets."""

        fact = {}
        for fact_key, widget in self.selectors[self.card_type.id]["widgets"]:
            start, end = widget.get_buffer().get_bounds()
            fact[fact_key] = widget.get_buffer().get_text(start, end)
        if check_for_required:
            for required in self.card_type.required_fields:
                if not fact[required]:
                    raise ValueError
        return fact

    def set_widgets_data(self, fact):
        """Set widgets data from fact."""

        for fact_key, widget in self.selectors[self.card_type.id]["widgets"]:
            widget.get_buffer().set_text(fact[fact_key])

    def clear_widgets(self):
        """Clear widgets data."""

        for caption in self.areas:
            self.areas[caption].get_buffer().set_text("<%s>" % caption.upper())

    def update_indicator(self):
        """Set non active state for widget."""

        self.get_widget("input_mode_snd_button").set_active(False)

    def hide_tags_dialog(self):
        """Close TagsDialog."""

        self.tag_mode = False
        tags_button = self.get_widget("tags_button")
        selected_tags = ", ".join([hbox.get_children()[1].get_label() for \
            hbox in self.get_widget("tags_box").get_children() \
                if hbox.get_children()[0].get_active()])
        tags_button.set_label(selected_tags or _("<default>"))
        tags_button.show()
        self.widgets["CardTypeSwitcher"].set_current_page(self.last_input_page)
        self.widgets["CardTypeButton"].set_sensitive(True)
        self.widgets["ContentButton"].set_sensitive(True)
        self.widgets["AddCardButton"].set_sensitive(True)
        return selected_tags

    # Callbacks

    def show_tags_dialog_cb(self, widget):
        """Show TagsDialog."""

        self.tag_mode = True
        tags_box = self.get_widget("tags_box")
        self.get_widget("tags_button").hide()
        self.last_input_page = self.widgets["CardTypeSwitcher"]. \
            get_current_page()
        self.widgets["CardTypeSwitcher"].set_current_page(3)
        self.widgets["CardTypeButton"].set_sensitive(False)
        self.widgets["ContentButton"].set_sensitive(False)
        self.widgets["AddCardButton"].set_sensitive(False)
        for child in tags_box.get_children():
            tags_box.remove(child)
        for tag in self.tags:
            tags_box.pack_start(self.create_tag_checkbox( \
                tag, tag in self.selected_tags))

    def add_new_tag_cb(self, widget):
        """Create new tag."""

        tag_entry = self.get_widget("new_tag_entry")
        tag = tag_entry.get_text()
        tags_box = self.get_widget("tags_box")
        if tag and not tag in self.tags:
            self.tags.append(tag)
            tag_widget = self.create_tag_checkbox(tag, True)
            tags_box.pack_start(tag_widget)
            tags_box.reorder_child(tag_widget, 0)
            tag_entry.set_text("")

    def show_cardtype_dialog_cb(self, widget):
        """Open CardTypeDialog."""

        for selector in self.selectors.values():
            selector["selector"].set_active( \
                self.card_type is selector["card_type"])
        get_widget = self.get_widget
        pos_x, pos_y = get_widget("imput_mode_cardtype_button"). \
            window.get_origin()
        get_widget("cardtype_dialog").move(pos_x, pos_y)
        get_widget("cardtype_dialog").show()
        self.main_widget().soundplayer.stop()

    def show_content_dialog_cb(self, widget):
        """Open ContentDialog."""

        get_widget = self.get_widget
        pos_x, pos_y = self.widgets["ContentButton"].window.get_origin()
        get_widget("content_dialog").move(pos_x, pos_y + get_widget( \
            "input_mode_toolbar_container").get_size_request()[1]/5)
        state = self.card_type.id in (FrontToBack.id)
        get_widget("sound_content_button").set_sensitive(state)
        get_widget("image_content_button").set_sensitive(state)
        get_widget("content_dialog").show()
        self.main_widget().soundplayer.stop()

    def set_card_type_cb(self, widget):
        """Sets current Card type and close CardTypesDialog."""

        self.get_widget("cardtype_dialog").hide()
        for selector in self.selectors.values():
            if selector['selector'].name == widget.name:
                selected_cardtype = selector['card_type']
                break
        self.set_card_type(selected_cardtype)
        if self.card_type.id is not FrontToBack.id:
            self.set_content_type("text")
        self.show_snd_container()
        self.clear_widgets()

    def set_content_type_cb(self, widget):
        """Sets current content type and close ContentDialog."""

        self.get_widget("content_dialog").hide()
        self.set_content_type(widget.name)
        self.get_widget("question_text_w").get_buffer().set_text("<QUESTION>")
        self.show_snd_container()

    def show_media_dialog_cb(self, widget, event):
        """Open MediaDialog."""

        if self.content_type == "text":
            if self.component_type == "add_cards_dialog":
                widget.get_buffer().set_text("")
        else:
            ctype = self.content_type + 'dir'
            setattr(self, ctype, self.conf[ctype])
            self.liststore.clear()
            self.get_widget("image_selection_dialog_button_select"). \
                set_sensitive(False)            
            self.get_widget("media_selection_dialog").show()
            if ctype == 'imagedir':
                for fname in os.listdir(self.imagedir):
                    if os.path.isfile(os.path.join(self.imagedir, fname)):
                        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size( \
                            os.path.join(self.imagedir, fname), 100, 100)
                        self.liststore.append(["", "img", fname, \
                            self.imagedir, pixbuf])
            else:
                self.main_widget().soundplayer.stop()
                for fname in os.listdir(self.sounddir):
                    if os.path.isfile(os.path.join(self.sounddir, fname)):
                        sound_logo_file = os.path.join( \
                            self.conf["theme_path"], "soundlogo.png")
                        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size( \
                            sound_logo_file, 100, 100)
                        self.liststore.append([fname, "sound", fname, \
                            self.sounddir, pixbuf])

    def enable_select_button_cb(self, widget):
        """If user has select item - enable Select button."""

        self.get_widget("image_selection_dialog_button_select"). \
            set_sensitive(True)
            
    def select_item_cb(self, widget):
        """Set html-text with media path and type when user
           select media filefrom media selection dialog."""

        self.get_widget("media_selection_dialog").hide()
        item_index = self.w_tree.get_widget("iconview_widget"). \
            get_selected_items()[0]
        item_type = self.liststore.get_value( \
            self.liststore.get_iter(item_index), 1)
        item_fname = self.liststore.get_value( \
            self.liststore.get_iter(item_index), 2)
        item_dirname = self.liststore.get_value( \
            self.liststore.get_iter(item_index), 3)
        question_text = """<%s src="%s">""" % \
            (item_type, os.path.abspath(os.path.join(item_dirname, item_fname)))
        self.areas["question"].get_buffer().set_text(question_text)
        self.show_snd_container()

    def preview_sound_in_input_cb(self, widget):
        """Listen sound in input mode."""

        if widget.get_active():
            start, end = self.areas["question"].get_buffer().get_bounds()
            text = self.areas["question"].get_buffer().get_text(start, end)
            self.main_widget().soundplayer.play(text, self)
        else:
            self.main_widget().soundplayer.stop()

    def close_media_selection_dialog_cb(self, widget):
        """Close MediaDialog."""

        self.get_widget("media_selection_dialog").hide()

    def input_to_main_menu_cb(self, widget):
        """Return to main menu."""

        pass


class NonBlockingAddCardsDialog(AddCardsDialog):
    """Non blocking variant of AddCardsDialog."""

    def add_cards(self):
        """This part is the first part of add_cards
           from default controller."""

        self.stopwatch().pause()
        self.component_manager.get_current("add_cards_dialog")\
            (self.component_manager).activate()

    def update_ui(self, review_controller):
        """This part is called from add_card_cb, when card is added."""

        self.database().save()
        review_controller.reload_counters()
        if review_controller.card is None:
            review_controller.new_question()
        else:
            review_controller.update_status_bar()
        self.stopwatch().unpause()


class AddCardsWidget(InputWidget, NonBlockingAddCardsDialog):
    """Add new card widget."""

    def __init__(self, component_manager):
        InputWidget.__init__(self, component_manager)
        NonBlockingAddCardsDialog.__init__(self, component_manager)
        self.connect_signals([\
            ("input_mode_toolbar_add_card_w", "button-press-event", \
                self.add_card_cb),
            ("answer_text_w", "button_press_event", self.clear_text_cb),
            ("pronun_text_w", "button_press_event", self.clear_text_cb),
            ("cloze_text_w", "button-press-event", self.clear_text_cb),
            ("foreign_text_w", "button-press-event", self.clear_text_cb),
            ("translation_text_w", "button-press-event", self.clear_text_cb),
            ("pronun_text_w", "button-press-event", self.clear_text_cb)])
        #FIXME: upstream exception?
        try:
            self.selected_tags = self.conf["tags_of_last_added"]
        except:
            self.selected_tags = _("<default>")

    def activate(self):
        """Activate input mode."""

        self.main_widget().soundplayer.stop()
        self.widgets["QuestionContainer"].show()
        self.widgets["SoundContainer"].hide()
        self.set_card_type(self.selectors[ \
            self.conf["card_type_last_selected"]]["card_type"])
        self.set_content_type(self.conf["content_type_last_selected"])
        self.update_tags()
        self.clear_widgets()

    @staticmethod
    def clear_text_cb(widget, event):
        """Clear textview content."""

        widget.get_buffer().set_text("")

    def add_card_cb(self, widget, event):
        """Add card to database."""

        # check for empty fields
        if not self.check_complete_input():
            return

        try:
            fact_data = self.get_widgets_data()
        except ValueError:
            return # Let the user try again to fill out the missing data.

        self.controller().create_new_cards(fact_data, self.card_type, -1, \
            [tag.strip() for tag in self.selected_tags.split(',')], save=True)
        self.clear_widgets()
        self.added_new_cards = True
        self.main_widget().soundplayer.stop()
        self.show_snd_container()
        self.update_ui(self.review_controller())

    def input_to_main_menu_cb(self, widget):
        """Return to main menu."""

        if self.tag_mode:
            self.selected_tags = self.hide_tags_dialog()            
        else:
            self.disconnect_signals()
            self.conf["tags_of_last_added"] = self.selected_tags
            self.conf["card_type_last_selected"] = self.card_type.id
            self.conf["content_type_last_selected"] = self.content_type
            self.conf.save()
            self.main_widget().soundplayer.stop()
            self.main_widget().menu_()


class NonBlockingEditFactDialog(EditFactDialog):
    """Non blocking variant of EditFactDialog
       edit_current_card is splitted to two methods."""

    def edit_current_card(self):
        """This part is the first part of edit_current_card
           from default controller."""

        self.stopwatch().pause()
        review_controller = self.review_controller()
        fact = review_controller.card.fact
        self.component_manager.get_current("edit_fact_dialog")\
            (fact, self.component_manager).activate()

    def update_ui(self, review_controller):
        """This part is called in callback, when editing is done."""

        review_controller.reload_counters()
        # Our current card could have disappeared from the database here,
        # e.g. when converting a front-to-back card to a cloze card, which
        # deletes the old cards and their learning history.        
        review_controller.card = self.database().get_card(\
            review_controller.card._id, id_is_internal=True)    
        review_controller.update_dialog(redraw_all=True)
        self.stopwatch().unpause()


class EditFactWidget(InputWidget, NonBlockingEditFactDialog):
    """Edit current fact widget."""

    def __init__(self, fact, component_manager, allow_cancel=True):
        InputWidget.__init__(self, component_manager)
        NonBlockingEditFactDialog.__init__(self, fact, 
            component_manager, allow_cancel)

        self.fact = fact
        self.selected_tags = self.database().cards_from_fact(fact)\
            [0].tag_string()
        self.allow_cancel = allow_cancel
        self.connect_signals([("input_mode_toolbar_add_card_w", 
            "button-press-event", self.update_card_cb)])

    def activate(self):
        """Activate input mode."""

        self.main_widget().soundplayer.stop()
        self.set_card_type(self.fact.card_type)
        if self.card_type.id is FrontToBack.id:
            if "img src=" in self.fact.data['q']:
                content_type = "image"
            elif "sound src=" in self.fact.data['q']:
                content_type = "sound"
            else:
                content_type = "text"
        else:
            content_type = "text"
            
        self.set_content_type(content_type)
        self.set_widgets_data(self.fact)
        self.update_tags()
        self.show_snd_container()

    def update_card_cb(self, widget, event):
        """Update card in the database."""

        try:
            fact_data = self.get_widgets_data()
        except ValueError:
            return # Let the user try again to fill out the missing data.

        new_tags = [tag.strip() for tag in self.selected_tags.split(',')]
        self.controller().update_related_cards(self.fact, fact_data,
          self.card_type, new_tags, None)
        self.review_controller().update_dialog(redraw_all=True)
        self.main_widget().activate_mode("review")
        self.main_widget().soundplayer.stop()
        self.show_snd_container()
        self.update_ui(self.review_controller())

    def input_to_main_menu_cb(self, widget):
        """Return to Review mode."""

        if self.tag_mode:
            self.selected_tags = self.hide_tags_dialog()
        else:
            self.disconnect_signals()
            self.main_widget().soundplayer.stop()
            self.main_widget().review_()


# Local Variables:
# mode: python
# py-indent-offset: 4
# indent-tabs-mode nil
# tab-width 4
# End:
