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

from mnemosyne.libmnemosyne.ui_components.review_widget import ReviewWidget
import mnemosyne.maemo_ui.widgets.review as widgets
from mnemosyne.maemo_ui import tts

LARGE_CONTAINER_HEIGHT = 260
NORMAL_CONTAINER_HEIGHT = 16

class ReviewWdgt(ReviewWidget):
    """Review Widget."""

    def __init__(self, component_manager):
        ReviewWidget.__init__(self, component_manager)
        self.sndtext = None
        self.tts = None
        self.renderer = self.component_manager.get_current('renderer')
        self.page, self.tts_button, self.edit_button, self.del_button, \
            self.question_container, self.answer_container, \
            self.question_text, self.answer_text, self.sound_container, \
            self.sound_button, self.grades_table, grades, toolbar_buttons, \
            self.tags_label = widgets.create_review_ui( \
                self.main_widget().switcher)
        self.tts_available = tts.is_available()
        self.tts_button.set_sensitive(self.tts_available)
        self.container_width = self.question_text.window.get_geometry()[2]
        # connect signals
        self.answer_text.connect('button-press-event', self.get_answer_cb)
        self.sound_button.connect('released', self.preview_sound_in_review_cb)
        for grade_button in grades:
            grade_button.connect('clicked', self.grade_cb)
        toolbar_buttons[0].connect('clicked', self.speak_cb)
        toolbar_buttons[1].connect('clicked', self.edit_card_cb)
        toolbar_buttons[2].connect('clicked', self.add_card_cb)
        toolbar_buttons[3].connect('clicked', self.statistics_card_cb)
        toolbar_buttons[4].connect('clicked', self.delete_card_cb)
        toolbar_buttons[5].connect('clicked', self.review_to_main_menu_cb)

    def activate(self):
        """Set necessary switcher page."""

        self.main_widget().switcher.set_current_page(self.page)

    def enable_edit_current_card(self, enabled):
        """Enable or disable 'edit card' button."""

        self.edit_button.set_sensitive(enabled)

    def enable_delete_current_card(self, enabled):
        """Enable or disable 'delete card' button."""

        self.del_button.set_sensitive(enabled)

    def set_question(self, text):
        """Set question."""

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
                self.question_container.set_size_request( \
                    self.container_width, LARGE_CONTAINER_HEIGHT)
            else:
                self.question_container.set_size_request( \
                    self.container_width, 16)
                self.tts_button.set_sensitive(self.tts_available)
            self.question_container.show()
        tags = [tag.name for tag in self.review_controller().card.tags]
        self.tags_label.set_text("Card tags: " + ', '.join(tags))
        self.renderer.render_html(self.question_text, text)

    def set_answer(self, text):
        """Set answer."""

        self.renderer.render_html(self.answer_text, text)

    def clear_question(self): 
        """Clear question text."""

        self.tags_label.set_text("No tags")
        self.renderer.render_html(self.question_text)

    def clear_answer(self):
        """Clear answer text."""

        self.renderer.render_html(self.answer_text)

    def update_show_button(self, text, default, enabled): 
        """Update show button."""

        self.answer_container.set_sensitive(enabled)
        if enabled:
            self.renderer.render_hint(self.answer_text, text)

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

        self.controller().add_cards()

    def statistics_card_cb(self, widget):
        """Hook for statistics of current card."""
        self.config()["last_variant_for_statistics_page"] = 0
        self.controller().show_statistics()

    def delete_card_cb(self, widget):
        """Hook for delete card."""

        self.main_widget().soundplayer.stop()
        self.controller().delete_current_fact()

    def edit_card_cb(self, widget):
        """Hook for edit card."""

        self.main_widget().soundplayer.stop()
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
