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

        # create widgets
        create_button = self.create_button
        toplevel_table = gtk.Table(rows=1, columns=2)
        toolbar_container = self.create_toolbar_container( \
            'input_mode_toolbar_container')
        toolbar_table = gtk.Table(rows=5, columns=1, homogeneous=True)
        card_type_button = create_button(None, self.show_cardtype_dialog_cb)
        content_button = create_button(None, self.show_content_dialog_cb)
        add_card_button = create_button('input_mode_toolbar_add_card_w')
        menu_button = create_button('input_mode_toolbar_button_back_w', \
            self.input_to_main_menu_cb)
        widgets_table = gtk.Table(rows=2, columns=1)
        widgets_table.set_row_spacings(14)
        tags_button = create_button('tags_button', self.show_tags_dialog_cb, \
            width=-1, height=60)
        card_type_switcher = gtk.Notebook()
        card_type_switcher.set_show_tabs(False)
        card_type_switcher.set_show_border(False)
        two_sided_box = gtk.VBox(spacing=10)
        sound_box = gtk.VBox()
        sound_box.set_homogeneous(True)
        sound_container = gtk.Table(rows=1, columns=3, homogeneous=True)
        sound_button = gtk.ToggleButton()
        sound_button.set_name('input_mode_snd_button')
        sound_button.connect('released', self.preview_sound_in_input_cb)
        question_container = gtk.Frame()
        question_container.set_name('input_mode_question_container')
        question_text = gtk.TextView()
        question_text.set_justification(gtk.JUSTIFY_CENTER)
        question_text.set_wrap_mode(gtk.WRAP_WORD)
        question_text.connect('button_release_event', self.show_media_dialog_cb)
        answer_container = gtk.Frame()
        answer_container.set_name('input_mode_answer_container')
        answer_text = gtk.TextView()
        answer_text.set_justification(gtk.JUSTIFY_CENTER)
        answer_text.set_wrap_mode(gtk.WRAP_WORD)
        three_sided_box = gtk.VBox(spacing=10)
        foreign_container = gtk.Frame()
        foreign_container.set_name('input_mode_foreign_container')
        foreign_text = gtk.TextView()
        foreign_text.set_justification(gtk.JUSTIFY_CENTER)
        foreign_text.set_wrap_mode(gtk.WRAP_WORD)
        pronunciation_container = gtk.Frame()
        pronunciation_container.set_name('input_mode_pronun_container')
        pronunciation_text = gtk.TextView()
        pronunciation_text.set_justification(gtk.JUSTIFY_CENTER)
        pronunciation_text.set_wrap_mode(gtk.WRAP_WORD)
        translation_container = gtk.Frame()
        translation_container.set_name('input_mode_translate_container')
        translation_text = gtk.TextView()
        translation_text.set_justification(gtk.JUSTIFY_CENTER)
        translation_text.set_wrap_mode(gtk.WRAP_WORD)
        cloze_box = gtk.VBox()
        cloze_container = gtk.Frame()
        cloze_container.set_name('input_mode_cloze_container')
        cloze_text = gtk.TextView()
        cloze_text.set_justification(gtk.JUSTIFY_CENTER)
        cloze_text.set_wrap_mode(gtk.WRAP_WORD)
        tags_layout = gtk.VBox(spacing=26)
        new_tag_box = gtk.HBox()
        new_tag_label = gtk.Label()
        new_tag_label.set_text('New tag: ')
        new_tag_label.set_name('new_tag_label')
        new_tag_button = create_button('new_tag_button', self.add_new_tag_cb, \
            width=60, height=60)
        new_tag_frame = gtk.Frame()
        new_tag_frame.set_name('new_tag_frame')
        new_tag_entry = gtk.Entry()
        new_tag_entry.set_name('new_tag_entry')
        tags_frame = gtk.Frame()
        tags_frame.set_name('tags_frame')
        tags_eventbox = gtk.EventBox()
        tags_eventbox.set_visible_window(True)
        tags_eventbox.set_name('tags_eventbox')
        tags_scrolledwindow = gtk.ScrolledWindow()
        tags_scrolledwindow.set_policy(gtk.POLICY_AUTOMATIC, \
            gtk.POLICY_AUTOMATIC)
        tags_scrolledwindow.set_name('tags_scrolledwindow')
        tags_viewport = gtk.Viewport()
        tags_viewport.set_name('tags_viewport')
        tags_box = gtk.VBox()
        tags_box.set_homogeneous(True)
        # packing widgets
        toolbar_table.attach(card_type_button, 0, 1, 0, 1, \
            xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
        toolbar_table.attach(content_button, 0, 1, 1, 2, \
            xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
        toolbar_table.attach(add_card_button, 0, 1, 2, 3, \
            xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
        toolbar_table.attach(menu_button, 0, 1, 4, 5, \
            xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
        toolbar_container.add(toolbar_table)
        toplevel_table.attach(toolbar_container, 0, 1, 0, 1, \
            xoptions=gtk.SHRINK, yoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL)
        widgets_table.attach(tags_button, 0, 1, 0, 1, \
            xoptions=gtk.SHRINK|gtk.FILL|gtk.EXPAND, \
            yoptions=gtk.SHRINK, xpadding=4)
        widgets_table.attach(card_type_switcher, 0, 1, 1, 2, \
            xoptions=gtk.SHRINK|gtk.FILL|gtk.EXPAND, \
            yoptions=gtk.SHRINK|gtk.FILL|gtk.EXPAND)
        card_type_switcher.append_page(two_sided_box)
        card_type_switcher.append_page(three_sided_box)
        card_type_switcher.append_page(cloze_box)
        card_type_switcher.append_page(tags_layout)
        sound_container.attach(sound_button, 1, 2, 0, 1, \
            xoptions=gtk.EXPAND|gtk.FILL, \
            yoptions=gtk.EXPAND|gtk.FILL|gtk.SHRINK)
        question_container.add(question_text)
        sound_box.pack_start(sound_container)
        sound_box.pack_end(question_container)
        answer_container.add(answer_text)
        two_sided_box.pack_start(sound_box)
        two_sided_box.pack_end(answer_container)
        foreign_container.add(foreign_text)
        pronunciation_container.add(pronunciation_text)
        translation_container.add(translation_text)
        three_sided_box.pack_start(foreign_container)
        three_sided_box.pack_start(pronunciation_container)
        three_sided_box.pack_end(translation_container)
        cloze_container.add(cloze_text)
        cloze_box.pack_start(cloze_container)
        new_tag_frame.add(new_tag_entry)
        new_tag_box.pack_start(new_tag_label, expand=False, fill=False, \
            padding=10)
        new_tag_box.pack_start(new_tag_frame, expand=True, fill=True, \
            padding=10)
        new_tag_box.pack_end(new_tag_button, expand=False, fill=False)
        tags_viewport.add(tags_box)
        tags_scrolledwindow.add(tags_viewport)
        tags_eventbox.add(tags_scrolledwindow)
        tags_frame.add(tags_eventbox)
        tags_layout.pack_start(new_tag_box, expand=False, fill=False)
        tags_layout.pack_end(tags_frame, expand=True, fill=True)
        toplevel_table.attach(widgets_table, 1, 2, 0, 1, \
            xoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL, xpadding=30, \
            yoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL, ypadding=30)
        toplevel_table.show_all()
        # hide necessary widgets
        sound_container.hide()
        self.page = self.main_widget().switcher.append_page(toplevel_table)

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
            "TagsButton": tags_button,
            "NewTagEntry": new_tag_entry,
            "TagsBox": tags_box,
            "CardTypeButton": card_type_button,
            "ContentButton": content_button,
            "CardTypeSwitcher": card_type_switcher,
            "AddCardButton": add_card_button,
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

        self.widgets["TagsButton"].set_label(', '.join( \
            [tag.strip() for tag in self.selected_tags.split(',') \
                if tag.strip() in self.tags]) or self.default_tag_name)

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

        self.widgets["SoundButton"].set_active(False)

    def hide_tags_dialog(self):
        """Close TagsDialog."""

        self.tag_mode = False
        selected_tags = ', '.join([hbox.get_children()[1].get_label() for \
            hbox in self.widgets["TagsBox"].get_children() if \
            hbox.get_children()[0].get_active()]) or self.default_tag_name
        self.widgets["TagsButton"].set_label(selected_tags)
        self.widgets["TagsButton"].show()
        self.widgets["CardTypeSwitcher"].set_current_page(self.last_input_page)
        for widget in ("CardTypeButton", "ContentButton", "AddCardButton"):
            self.widgets[widget].set_sensitive(True)
        return selected_tags

    # Callbacks

    def show_tags_dialog_cb(self, widget):
        """Show TagsDialog."""

        self.tag_mode = True
        tags_box = self.widgets["TagsBox"]
        self.widgets["TagsButton"].hide()
        self.last_input_page = self.widgets["CardTypeSwitcher"]. \
            get_current_page()
        self.widgets["CardTypeSwitcher"].set_current_page(3)
        for widget in ("CardTypeButton", "ContentButton", "AddCardButton"):
            self.widgets[widget].set_sensitive(False)
        for child in tags_box.get_children():
            tags_box.remove(child)
        for tag in self.tags:
            tags_box.pack_start(self.create_tag_checkbox( \
                tag, tag in self.selected_tags))

    def add_new_tag_cb(self, widget):
        """Create new tag."""

        tag_entry = self.widgets["NewTagEntry"]
        tag = tag_entry.get_text()
        tags_box = self.widgets["TagsBox"]
        if tag and not tag in self.tags:
            self.tags.append(tag)
            tag_widget = self.create_tag_checkbox(tag, True)
            tags_box.pack_start(tag_widget)
            tags_box.reorder_child(tag_widget, 0)
            tag_entry.set_text("")

    def show_cardtype_dialog_cb(self, widget):
        """Open CardTypeDialog."""

        self.main_widget().soundplayer.stop()
        create_button = self.create_radio_button
        button = create_button(None, 'front_to_back_cardtype_button', \
            self.set_card_type_cb)
        self.selectors[FrontToBack.id]['selector'] = button
        button = create_button(button, 'both_ways_cardtype_button', \
            self.set_card_type_cb)
        self.selectors[BothWays.id]['selector'] = button
        button = create_button(button, 'three_sided_cardtype_button', \
            self.set_card_type_cb)
        self.selectors[ThreeSided.id]['selector'] = button
        button = create_button(button, 'cloze_cardtype_button', \
            self.set_card_type_cb)
        self.selectors[Cloze.id]['selector'] = button
        dialog = gtk.Dialog()
        dialog.set_decorated(False)
        dialog.set_has_separator(False)
        pos_x, pos_y = self.widgets['CardTypeButton'].window.get_origin()
        dialog.move(pos_x, pos_y)
        buttons_table = gtk.Table(rows=1, columns=4, homogeneous=True)
        buttons_table.set_col_spacings(16)
        index = 0
        for selector in self.selectors.values():
            widget = selector['selector']
            if self.card_type is selector['card_type']:
                widget.set_active(True)
            buttons_table.attach(widget, index, index + 1, 0, 1, \
                xoptions=gtk.EXPAND, xpadding=6)
            index += 1
        dialog.vbox.pack_start(buttons_table, expand=True, fill=False, \
            padding=12)
        buttons_table.show_all()
        dialog.run()

    def show_content_dialog_cb(self, widget):
        """Open ContentDialog."""

        self.main_widget().soundplayer.stop()
        create_button = self.create_button
        text_content_button = create_button('text_content_button', \
            self.set_content_type_cb, width=72, height=72)
        image_content_button = create_button('image_content_button', \
            self.set_content_type_cb, width=72, height=72)
        sound_content_button = create_button('sound_content_button', \
            self.set_content_type_cb, width=72, height=72)
        dialog = gtk.Dialog()
        dialog.set_decorated(False)
        dialog.set_has_separator(False)
        pos_x, pos_y = self.widgets["ContentButton"].window.get_origin()
        dialog.move(pos_x, pos_y + \
            self.widgets["ToolbarContainer"].get_size_request()[1]/5)
        state = self.card_type.id in (FrontToBack.id)
        sound_content_button.set_sensitive(state)
        image_content_button.set_sensitive(state)
        buttons_table = gtk.Table(rows=1, columns=3, homogeneous=True)
        buttons_table.set_col_spacings(16)
        buttons_table.attach(text_content_button, 0, 1, 0, 1, \
                xoptions=gtk.EXPAND, xpadding=10)
        buttons_table.attach(sound_content_button, 1, 2, 0, 1, \
                xoptions=gtk.EXPAND, xpadding=10)
        buttons_table.attach(image_content_button, 2, 3, 0, 1, \
                xoptions=gtk.EXPAND, xpadding=10)
        buttons_table.show_all()
        dialog.vbox.pack_start(buttons_table, expand=True, fill=False, \
            padding=8)
        dialog.run()

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
        self.areas['question'].get_buffer().set_text("<QUESTION>")
        self.show_snd_container()

    def show_media_dialog_cb(self, widget, event):
        """Open MediaDialog."""

        if self.content_type == "text":
            if self.component_type == "add_cards_dialog":
                widget.get_buffer().set_text("")
        else:
            def enable_select_button_cb(widget, select_button):
                """If user has select item - enable Select button."""
                select_button.set_sensitive(True)

            ctype = self.content_type + 'dir'
            setattr(self, ctype, self.conf[ctype])
            #liststore = [text, type, filename, dirname, pixbuf]
            liststore = gtk.ListStore(str, str, str, str, gtk.gdk.Pixbuf)
            dialog = gtk.Dialog()
            dialog.set_decorated(False)
            dialog.set_has_separator(False)
            dialog.resize(510, 420)
            width, height = dialog.get_size()
            dialog.move((gtk.gdk.screen_width() - width)/2, \
                (gtk.gdk.screen_height() - height)/2)
            iconview_widget = gtk.IconView()
            iconview_widget.set_name('iconview_widget')
            iconview_widget.set_model(liststore)
            iconview_widget.set_pixbuf_column(4)
            iconview_widget.set_text_column(0)
            label = gtk.Label('Select media')
            label.set_name('media_selection_dialog_label')
            scrolledwindow_widget = gtk.ScrolledWindow()
            scrolledwindow_widget.set_policy(gtk.POLICY_NEVER, \
                gtk.POLICY_AUTOMATIC)
            scrolledwindow_widget.set_name('scrolledwindow_widget')
            scrolledwindow_widget.add(iconview_widget)
            widgets_table = gtk.Table(rows=1, columns=1)
            widgets_table.attach(scrolledwindow_widget, 0, 1, 0, 1, \
                xpadding=12, ypadding=12)
            dialog.vbox.pack_start(label, expand=False, fill=False, padding=5)
            dialog.vbox.pack_start(widgets_table)
            dialog.vbox.show_all()
            select_button = dialog.add_button('Select', gtk.RESPONSE_OK)
            select_button.set_size_request(232, 60)
            select_button.set_sensitive(False)            
            select_button.set_name('dialog_button')
            iconview_widget.connect('selection-changed', \
                enable_select_button_cb, select_button)
            cancel_button = dialog.add_button('Cancel', gtk.RESPONSE_REJECT)
            cancel_button.set_size_request(232, 60)
            cancel_button.set_name('dialog_button')
            dialog.action_area.set_layout(gtk.BUTTONBOX_SPREAD)
            if ctype == 'imagedir':
                for fname in os.listdir(self.imagedir):
                    if os.path.isfile(os.path.join(self.imagedir, fname)):
                        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size( \
                            os.path.join(self.imagedir, fname), 100, 100)
                        liststore.append(["", "img", fname, self.imagedir, \
                            pixbuf])
            else:
                self.main_widget().soundplayer.stop()
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
                item_type = liststore.get_value( \
                    liststore.get_iter(item_index), 1)
                item_fname = liststore.get_value( \
                    liststore.get_iter(item_index), 2)
                item_dirname = liststore.get_value( \
                    liststore.get_iter(item_index), 3)
                question_text = """<%s src="%s">""" % (item_type, \
                    os.path.abspath(os.path.join(item_dirname, item_fname)))
                self.areas["question"].get_buffer().set_text(question_text)
                self.show_snd_container()
            dialog.destroy()

    def preview_sound_in_input_cb(self, widget):
        """Listen sound in input mode."""

        if widget.get_active():
            start, end = self.areas["question"].get_buffer().get_bounds()
            text = self.areas["question"].get_buffer().get_text(start, end)
            self.main_widget().soundplayer.play(text, self)
        else:
            self.main_widget().soundplayer.stop()

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
        self.widgets['AddCardButton'].connect('clicked', self.add_card_cb)
        for name in ('answer', 'foreign', 'pronunciation', 'translation', \
            'cloze'):
            self.areas[name].connect('button_press_event', self.clear_text_cb)
        try:
            self.selected_tags = self.conf["tags_of_last_added"]
        except:
            self.selected_tags = self.default_tag_name

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
        self.main_widget().switcher.set_current_page(self.page)

    @staticmethod
    def clear_text_cb(widget, event):
        """Clear textview content."""

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
            #self.conf["tags_of_last_added"] = self.selected_tags
            self.conf["card_type_last_selected"] = self.card_type.id
            self.conf["content_type_last_selected"] = self.content_type
            self.conf.save()
            self.main_widget().soundplayer.stop()
            self.main_widget().switcher.remove_page(self.page)
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
        self.widgets['AddCardButton'].connect('clicked', self.update_card_cb)

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
        self.main_widget().switcher.set_current_page(self.page)

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
        self.main_widget().activate_mode("review")
        self.main_widget().soundplayer.stop()
        self.show_snd_container()
        self.update_ui(self.review_controller())

    def input_to_main_menu_cb(self, widget):
        """Return to Review mode."""

        if self.tag_mode:
            self.selected_tags = self.hide_tags_dialog()
        else:
            self.main_widget().soundplayer.stop()
            self.main_widget().switcher.remove_page(self.page)
            self.main_widget().review_()


# Local Variables:
# mode: python
# py-indent-offset: 4
# indent-tabs-mode nil
# tab-width 4
# End:
