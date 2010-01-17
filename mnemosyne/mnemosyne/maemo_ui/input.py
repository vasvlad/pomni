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

from mnemosyne.libmnemosyne.ui_components.dialogs import \
    AddCardsDialog, EditFactDialog
import mnemosyne.maemo_ui.widgets.input as widgets
from mnemosyne.libmnemosyne.ui_component import UiComponent
from mnemosyne.libmnemosyne.utils import numeric_string_cmp
from mnemosyne.libmnemosyne.card_types.front_to_back import FrontToBack
from mnemosyne.libmnemosyne.card_types.both_ways import BothWays
from mnemosyne.libmnemosyne.card_types.three_sided import ThreeSided
from mnemosyne.libmnemosyne.card_types.cloze import Cloze
Cloze.required_fields = ["text"]

_ = gettext.gettext

FONT_DISTINCTION = 7

class InputWidget(UiComponent):
    """Input mode widget for Rainbow theme."""
    
    def __init__(self, component_manager):

        UiComponent.__init__(self, component_manager)
        self.conf = self.config()
        self.default_tag_name = _("<default>")
        self.content_type = None
        self.last_input_page = None
        self.fact = None
        self.tag_mode = False
        self.sounddir = None
        self.imagedir = None
        self.card_type = None
        self.selected_tags = None
        self.tags = sorted(self.database().get_tag_names(), \
            cmp=numeric_string_cmp) or [self.default_tag_name]
        self.added_new_cards = False
        self._main_widget = self.main_widget()
        self._main_widget.soundplayer.stop()
        # create widgets
        self.page, card_type_button, content_button, menu_button, tags_button, \
            sound_button, question_text, answer_text, foreign_text, \
            pronunciation_text, translation_text, cloze_text, new_tag_button, \
            new_tag_entry, tags_box, card_type_switcher, sound_container, \
            question_container, toolbar_container, self.grades, tags_label, \
            tags_button = widgets.create_input_ui(self._main_widget.switcher, \
                self.conf["theme_path"])
        
        # connect signals
        card_type_button.connect('clicked', self.show_cardtype_dialog_cb)
        content_button.connect('clicked', self.show_content_dialog_cb)
        menu_button.connect('clicked', self.input_to_main_menu_cb)
        tags_button.connect('clicked', self.show_tags_dialog_cb)
        sound_button.connect('button-press-event', self.preview_sound_in_input_cb)
        question_text.connect('button_release_event', self.show_media_dialog_cb)
        new_tag_button.connect('clicked', self.add_new_tag_cb)
        
        # create language switcher and set its callbacks for all text widgets
        text_widgets = [question_text, answer_text, foreign_text,
                        pronunciation_text, translation_text, cloze_text]
        langswitcher = self.component_manager.get_current("langswitcher")
        for widget in text_widgets:
            widget.connect('focus-in-event', langswitcher.restore_cb)
            widget.connect('focus-out-event', langswitcher.save_cb)

        # Widgets as attributes
        self.areas = {"cloze": cloze_text, "answer":  answer_text,
            "foreign": foreign_text, "pronunciation": pronunciation_text,
            "translation": translation_text, "question": question_text}

        # Change default font
        font = pango.FontDescription("Nokia Sans %s" % \
            (self.conf['font_size'] - FONT_DISTINCTION))
        for area in self.areas.values():
            area.modify_font(font)

        self.widgets = {# Other widgets
            "TagsLabel": tags_label,
            "TagsButton": tags_button,
            "NewTagEntry": new_tag_entry,
            "TagsBox": tags_box,
            "CardTypeButton": card_type_button,
            "ContentButton": content_button,
            "CardTypeSwitcher": card_type_switcher,
            "SoundContainer": sound_container,
            "SoundButton": sound_button,
            "QuestionContainer": question_container,
            "ToolbarContainer": toolbar_container}

        # card_id: {"page": page_id, "selector": selector_widget, 
        # "widgets": [(field_name:text_area_widget)...]}
        self.selectors = {
            FrontToBack.id: {
                "page": 0, 
                "selector": None,
                "widgets": [('q', question_text), ('a', answer_text)]},
            BothWays.id: {
                "page": 0,
                "selector": None,
                "widgets": [('q', question_text), ('a', answer_text)]},
            ThreeSided.id: {
                "page": 1,
                "selector": None,
                "widgets": [('f', foreign_text), ('t', translation_text),
                    ('p', pronunciation_text)]},
            Cloze.id: {
                "page": 2,
                "selector": None,
                "widgets": [('text', self.areas["cloze"])]}
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
        """Show or hide sound button. """
                    
        text = self.get_textview_text(self.areas["question"])
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

        tags = ', '.join([tag.strip() for tag in self.selected_tags.split(',') \
            if tag.strip() in self.tags]) or self.default_tag_name
        self.widgets["TagsLabel"].set_text(_('Current tags: ') + tags)

    def check_complete_input(self):
        """Check for non empty fields."""

        pattern_list = ["<%s>" % caption.upper() for caption in self.areas]
        pattern_list.append("")
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
            fact[fact_key] = self.get_textview_text(widget)
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

    def get_textview_text(self, widget):
        """Returns current text in textview."""

        start, end = widget.get_buffer().get_bounds()
        return widget.get_buffer().get_text(start, end)

    def hide_tags_dialog(self):
        """Close TagsDialog."""

        self.tag_mode = False
        selected_tags = ', '.join([hbox.get_children()[1].get_label() for \
            hbox in self.widgets["TagsBox"].get_children() if \
            hbox.get_children()[0].get_active()]) or self.default_tag_name
        self.widgets["TagsLabel"].set_text(_('Current tags: ') + selected_tags)
        self.widgets["TagsLabel"].show()
        self.widgets["CardTypeSwitcher"].set_current_page(self.last_input_page)
        for widget in ("CardTypeButton", "ContentButton", "TagsButton"):
            self.widgets[widget].set_sensitive(True)
        for widget in self.grades.values():
            widget.set_sensitive(True)
        return selected_tags

    # Callbacks

    def show_tags_dialog_cb(self, widget):
        """Show TagsDialog."""

        self.tag_mode = True
        tags_box = self.widgets["TagsBox"]
        self.widgets["TagsLabel"].hide()
        self.last_input_page = self.widgets["CardTypeSwitcher"]. \
            get_current_page()
        self.widgets["CardTypeSwitcher"].set_current_page(3)
        for widget in ("CardTypeButton", "ContentButton", "TagsButton"):
            self.widgets[widget].set_sensitive(False)
        for widget in self.grades.values():
            widget.set_sensitive(False)
        for child in tags_box.get_children():
            tags_box.remove(child)
        for tag in self.tags:
            tags_box.pack_start(widgets.create_tag_checkbox( \
                tag, tag in self.selected_tags))

    def add_new_tag_cb(self, widget):
        """Create new tag."""

        tag_entry = self.widgets["NewTagEntry"]
        tag = tag_entry.get_text()
        tags_box = self.widgets["TagsBox"]
        if tag and not tag in self.tags:
            self.tags.append(tag)
            tag_widget = widgets.create_tag_checkbox(tag, True)
            tags_box.pack_start(tag_widget)
            tags_box.reorder_child(tag_widget, 0)
            tag_entry.set_text("")

    def show_cardtype_dialog_cb(self, widget):
        """Open CardTypeDialog."""

        self._main_widget.soundplayer.stop()
        widgets.create_card_type_dialog_ui(self.selectors, FrontToBack.id, \
            BothWays.id, ThreeSided.id, Cloze.id, self.widgets[ \
            'CardTypeButton'], self.card_type, self.set_card_type_cb)

    def show_content_dialog_cb(self, widget):
        """Open ContentDialog."""

        self._main_widget.soundplayer.stop()
        widgets.create_content_dialog_ui(self.set_content_type_cb,
            self.widgets["ContentButton"], self.widgets["ToolbarContainer"],
            self.card_type, FrontToBack.id)

    def set_card_type_cb(self, widget):
        """Sets current Card type and close CardTypesDialog."""

        widget.get_parent().get_parent().get_parent().destroy()
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

        widget.get_parent().get_parent().get_parent().destroy()
        self.set_content_type(widget.name)
        self.areas['question'].get_buffer().set_text(_("<QUESTION>"))
        self.show_snd_container()

    def set_current_grade_cb(self, widget):
        """Sets current grade value."""

        self.set_current_grade(int(widget.name[5]))

    def show_media_dialog_cb(self, widget, event):
        """Open MediaDialog."""

        if self.content_type == "text":
            if self.component_type == "add_cards_dialog":
                if self.get_textview_text(widget) in ["<%s>" % caption.upper() \
                    for caption in self.areas]:
                    widget.get_buffer().set_text("")
        else:
            ctype = self.content_type + 'dir'
            setattr(self, ctype, self.conf[ctype])
            dialog, liststore, iconview_widget = widgets.create_media_dialog_ui()
            if ctype == 'imagedir':
                for fname in os.listdir(self.imagedir):
                    if os.path.isfile(os.path.join(self.imagedir, fname)):
                        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size( \
                            os.path.join(self.imagedir, fname), 100, 100)
                        liststore.append(["", "img", fname, self.imagedir, \
                            pixbuf])
            else:
                self._main_widget.soundplayer.stop()
                for fname in os.listdir(self.sounddir):
                    if os.path.isfile(os.path.join(self.sounddir, fname)):
                        sound_logo_file = os.path.join( \
                            self.conf["theme_path"], "soundlogo.png")
                        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size( \
                            sound_logo_file, 100, 100)
                        liststore.append([fname, "sound", fname, \
                            self.sounddir, pixbuf])
            response = dialog.run()
            if response == gtk.RESPONSE_OK:
                item_index = iconview_widget.get_selected_items()[0]
                item_type = liststore.get_value(liststore.get_iter( \
                    item_index), 1)
                item_fname = liststore.get_value(liststore.get_iter( \
                    item_index), 2)
                item_dirname = liststore.get_value(liststore.get_iter( \
                    item_index), 3)
                question_text = """<%s src="%s">""" % (item_type, \
                    os.path.abspath(os.path.join(item_dirname, item_fname)))
                self.areas["question"].get_buffer().set_text(question_text)
                self.show_snd_container()
            dialog.destroy()

    def preview_sound_in_input_cb(self, widget, event):
        """Listen sound in input mode."""

        if self._main_widget.soundplayer.stopped():
            self._main_widget.soundplayer.play(self.get_textview_text( \
                self.areas["question"]), self)
        else:
            self._main_widget.soundplayer.stop()

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
        # connect signals
        for button in self.grades.values():
            button.connect('clicked', self.add_card_cb)
        for name in ('answer', 'foreign', 'pronunciation', 'translation', \
            'cloze'):
            self.areas[name].connect('button_press_event', self.clear_text_cb)
        # gets last selected options
        try:
            self.selected_tags = self.conf["tags_of_last_added"]
            self.last_selected_grade = self.conf['last_selected_grade']
        except:
            self.selected_tags = self.default_tag_name
            self.last_selected_grade = 0

    def activate(self):
        """Activate input mode."""

        self.show_snd_container()
        self.set_card_type(self.selectors[ \
            self.conf["card_type_last_selected"]]["card_type"])
        self.set_content_type(self.conf["content_type_last_selected"])
        self.update_tags()
        self.clear_widgets()
        self._main_widget.switcher.set_current_page(self.page)

    def clear_text_cb(self, widget, event):
        """Clear textview content."""

        if self.get_textview_text(widget) in ["<%s>" % caption.upper() \
            for caption in self.areas]:
            widget.get_buffer().set_text("")

    def add_card_cb(self, widget):
        """Add card to database."""

        # check for empty fields
        if not self.check_complete_input():
            return

        try:
            fact_data = self.get_widgets_data()
        except ValueError:
            return # Let the user try again to fill out the missing data.

        grade = int(widget.name[-1])
        if grade in (0, 1):
            grade = -1
        self.controller().create_new_cards(fact_data, self.card_type, grade, \
            [tag.strip() for tag in self.selected_tags.split(',')], save=True)
        self.added_new_cards = True
        self._main_widget.soundplayer.stop()
        self.clear_widgets()
        self.show_snd_container()
        self.update_ui(self.review_controller())

    def input_to_main_menu_cb(self, widget):
        """Return to main menu."""

        if self.tag_mode:
            self.selected_tags = self.hide_tags_dialog()            
        else:
            self.conf["tags_of_last_added"] = self.selected_tags
            self.conf["last_selected_grade"] = self.last_selected_grade
            self.conf["card_type_last_selected"] = self.card_type.id
            self.conf["content_type_last_selected"] = self.content_type
            self.conf.save()
            self._main_widget.soundplayer.stop()
            self._main_widget.switcher.remove_page(self.page)
            self._main_widget.menu_()


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
        self.allow_cancel = allow_cancel
        self.selected_tags = self.database().cards_from_fact(fact)\
            [0].tag_string()
        # set grade of the current card active
        for num in range(6):
            self.grades[num].set_name('grade%s_disabled' % num)
        current_grade = self.review_controller().card.grade
        if current_grade == -1:
            current_grade = 0
        self.grades[current_grade].set_name('grade%s' % current_grade)
        # connect signals
        self.grades[current_grade].connect('clicked', self.update_card_cb)

    def activate(self):
        """Activate input mode."""

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
        self._main_widget.switcher.set_current_page(self.page)

    def update_card_cb(self, widget):
        """Update card in the database."""

        try:
            fact_data = self.get_widgets_data()
        except ValueError:
            return # Let the user try again to fill out the missing data.

        new_tags = [tag.strip() for tag in self.selected_tags.split(',')]
        self.controller().update_related_cards(self.fact, fact_data,
          self.card_type, new_tags, None)
        self.review_controller().update_dialog(redraw_all=True)
        self._main_widget.activate_mode("review")
        self._main_widget.soundplayer.stop()
        self.show_snd_container()
        self.update_ui(self.review_controller())

    def input_to_main_menu_cb(self, widget):
        """Return to Review mode."""

        if self.tag_mode:
            self.selected_tags = self.hide_tags_dialog()
        else:
            self._main_widget.soundplayer.stop()
            self._main_widget.switcher.remove_page(self.page)
            self._main_widget.review_()


# Local Variables:
# mode: python
# py-indent-offset: 4
# indent-tabs-mode nil
# tab-width 4
# End:
