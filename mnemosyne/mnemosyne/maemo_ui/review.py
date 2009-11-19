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
Hildon UI. Review widgets.
"""

import gtk
from mnemosyne.libmnemosyne.ui_components.review_widget import ReviewWidget
from mnemosyne.maemo_ui import tts

LARGE_CONTAINER_HEIGHT = 260
NORMAL_CONTAINER_HEIGHT = 16

class ReviewWdgt(ReviewWidget):
    """Review Widget."""

    def __init__(self, component_manager):
        ReviewWidget.__init__(self, component_manager)
        self.next_is_image_card = False #Image card indicator
        self.sndtext = None
        self.tts = None
        self.renderer = self.component_manager.get_current('renderer')

        def create_button(name, callback, event='clicked', width=80, height=80):
            button = gtk.Button()
            button.set_size_request(width, height)
            button.set_name(name)
            button.connect(event, callback)
            return button

        # create widgets
        toplevel_table = gtk.Table(rows=1, columns=3)
        toolbar_container = gtk.Notebook()
        toolbar_container.set_show_tabs(False)
        toolbar_container.set_size_request(82, 480)
        toolbar_container.set_name('review_mode_toolbar_container')
        grades_container = gtk.Notebook()
        grades_container.set_show_tabs(False)
        grades_container.set_size_request(82, 480)
        grades_container.set_name('review_mode_grades_container')
        toolbar_table = gtk.Table(rows=5, columns=1, homogeneous=True)
        grades_table = gtk.Table(rows=6, columns=1, homogeneous=True)
        widgets_box = gtk.VBox(spacing=10)
        question_box = gtk.VBox(homogeneous=True)
        sound_container = gtk.Table(rows=1, columns=10, homogeneous=True)
        sound_button = gtk.Button()
        answer_container = gtk.Frame()
        answer_container.set_name('answer_container')
        question_container = gtk.Frame()
        question_container.set_name('question_container')
        answer_text = self.main_widget().create_gtkhtml()
        question_text = self.main_widget().create_gtkhtml()
        # create toolbar buttons
        buttons = {}
        buttons[0] = create_button('review_toolbar_tts_button', self.speak_cb)
        buttons[1] = create_button('review_toolbar_edit_card_button', \
            self.edit_card_cb)
        buttons[2] = create_button('review_toolbar_add_card_button', \
            self.add_card_cb)
        buttons[3] = create_button('review_toolbar_delete_card_button', \
            self.delete_card_cb)
        buttons[4] = create_button('review_toolbar_main_menu_button', \
           self.review_to_main_menu_cb) 
        # create grades buttons
        grades = {}
        for num in range(6):
            grades[num] = create_button('grade%s' % num, self.grade_cb)
        # packing toolbar buttons
        for pos in buttons.keys():
            toolbar_table.attach(buttons[pos], 0, 1, pos, pos + 1, \
                xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
        toolbar_container.add(toolbar_table)
        # packing grades buttons
        for pos in grades.keys():
            grades_table.attach(grades[pos], 0, 1, 5 - pos, 6 - pos, \
                xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
        grades_container.add(grades_table)
        toplevel_table.attach(toolbar_container, 0, 1, 0, 1, \
            xoptions=gtk.SHRINK, yoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL)
        toplevel_table.attach(grades_container, 3, 4, 0, 1, \
            xoptions=gtk.SHRINK, yoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL)
        question_container.add(question_text)
        answer_container.add(answer_text)
        sound_container.attach(sound_button, 3, 7, 0, 1, \
            xoptions=gtk.EXPAND|gtk.FILL|gtk.SHRINK, \
            yoptions=gtk.EXPAND|gtk.FILL|gtk.SHRINK)
        question_box.pack_start(sound_container)
        question_box.pack_end(question_container)
        widgets_box.pack_start(question_box)
        widgets_box.pack_end(answer_container)
        toplevel_table.attach(widgets_box, 2, 3, 0, 1, ypadding=30,
            xoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL, \
            yoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL, xpadding=30)
        toplevel_table.show_all()
        self.main_widget().switcher.insert_page(toplevel_table, position=1)
        # create class attributes
        self.tts_button, self.edit_button, self.del_button = buttons[0], \
            buttons[1], buttons[3]
        self.tts_available = tts.is_available()
        self.tts_button.set_sensitive(self.tts_available)
        self.question_container, self.answer_container = question_container, \
            answer_container
        self.question_text, self.answer_text = question_text, answer_text
        self.container_width = question_text.window.get_geometry()[2]
        self.sound_container = sound_container
        self.sound_button = sound_button
        self.grades_table = grades_table
        # connect signals
        answer_text.connect('button-press-event', self.get_answer_cb)
        sound_button.connect('released', self.preview_sound_in_review_cb)

    def activate(self):
        self.main_widget().switcher.set_current_page(1)

    def enable_edit_current_card(self, enabled):
        """Enable or disable 'edit card' button."""

        self.edit_button.set_sensitive(enabled)
        
    def enable_delete_current_card(self, enabled):
        """Enable or disable 'delete card' button."""

        self.del_button.set_sensitive(enabled)
        
    def set_question(self, text):
        """Set question."""
        
        self.next_is_image_card = False
        self.tts_button.set_sensitive(False)
        if "sound src=" in text:
            self.sndtext = text
            self.question_container.hide()
            self.sound_container.set_size_request( \
                self.container_width, NORMAL_CONTAINER_HEIGHT)
            self.sound_container.show()
            self.sound_button.set_active(True)
            self.main_widget().soundplayer.play(self.sndtext, self)
        else:
            self.sound_container.hide()            
            if "img src=" in text:
                self.next_is_image_card = True
                self.question_container.set_size_request( \
                    self.container_width, LARGE_CONTAINER_HEIGHT)
            else:
                self.question_container.set_size_request( \
                    self.container_width, 16)
                self.tts_button.set_sensitive(self.tts_available)
            self.question_container.show()
        self.renderer.render_html(self.question_text, text)

    def set_answer(self, text):
        """Set answer."""

        self.renderer.render_html(self.answer_text, text)
        
    def clear_question(self): 
        """Clear question text."""

        self.renderer.render_html(self.question_text)
        
    def clear_answer(self):
        """Clear answer text."""

        self.renderer.render_html(self.answer_text)
        
    def update_show_button(self, text, default, enabled): 
        """Update show button."""

        self.answer_container.set_sensitive(enabled)
        if enabled:
            self.renderer.render_hint( \
                self.answer_text, text, self.next_is_image_card)

    def enable_grades(self, enabled):
        """Enable grades."""

        self.grades_table.set_sensitive(enabled)
        self.enable_edit_current_card(enabled)
        self.enable_delete_current_card(enabled)

    def update_indicator(self):
        """Set non active state for widget."""

        self.sound_button.set_active(False)

    # callbacks
    def speak_cb(self, widget):
        """Speaks current question."""

        config = self.config()
        params = {"language": config['tts_language'], "voice": \
            config['tts_voice'], "speed": config['tts_speed'], \
            "pitch": config['tts_pitch']}
        if not self.tts:            
            self.tts = tts.TTS(params['language'], params['voice'], 
                params['pitch'], params['speed'])
        self.tts.set_params(params)
        self.tts.speak(self.renderer.tts_text)

    def preview_sound_in_review_cb(self, widget):
        """Play/stop listening."""

        if widget.get_active():
            self.main_widget().soundplayer.play(self.sndtext, self)
        else:
            self.main_widget().soundplayer.stop()

    def review_to_main_menu_cb(self, widget):
        """Return to main menu."""

        self.main_widget().soundplayer.stop()
        self.main_widget().menu_()

    def get_answer_cb(self, widget, event):
        """Hook for showing a right answer."""

        self.review_controller().show_answer()

    def add_card_cb(self, widget):
        """Hook for add new card."""

        self.main_widget().show_mode("input")
        self.controller().add_cards()

    def delete_card_cb(self, widget):
        """Hook for delete card."""

        self.main_widget().soundplayer.stop()
        self.controller().delete_current_fact()

    def edit_card_cb(self, widget):
        """Hook for edit card."""

        self.main_widget().soundplayer.stop()
        self.main_widget().show_mode("input")
        self.controller().edit_current_card()

    def grade_cb(self, widget):
        """Call grade of answer."""

        self.main_widget().soundplayer.stop()
        self.review_controller().grade_answer(int(widget.name[-1]))


# Local Variables:
# mode: python
# py-indent-offset: 4
# indent-tabs-mode nil
# tab-width 4
# End:
