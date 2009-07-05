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
Hildon UI. Review widgets.
"""

import gettext

from mnemosyne.libmnemosyne.ui_components.review_widget import ReviewWidget

_ = gettext.gettext

LARGE_CONTAINER_HEIGHT = 260
NORMAL_CONTAINER_HEIGHT = 16

class RainbowReviewWidget(ReviewWidget):
    """Rainbow theme: Review Widget."""

    def __init__(self, component_manager):
        ReviewWidget.__init__(self, component_manager)
        self.w_tree = self.main_widget().w_tree
        self.w_tree.signal_autoconnect( \
            dict([(sig, getattr(self, sig + "_cb")) \
                for sig in ["review_to_main_menu", "get_answer", "grade", 
                "delete_card", "edit_card", "preview_sound_in_review"]]))
        self.next_is_image_card = False #Image card indicator
        self.sndtext = None
        self.renderer = self.component_manager.get_current('renderer')

        # Widgets as attributes
        self.question_container = self.w_tree.get_widget("question_container")
        self.answer_container = self.w_tree.get_widget("answer_container")
        self.container_width = self.w_tree.get_widget( \
            "question_text").window.get_geometry()[2]
        self.question_text = self.w_tree.get_widget("question_text")
        self.answer_text = self.w_tree.get_widget("answer_text")
        self.sound_container = self.w_tree.get_widget( \
            "review_mode_snd_container")
        self.sound_button = self.w_tree.get_widget("review_mode_snd_button")
        self.grades_table = self.w_tree.get_widget("grades_table")

    def activate(self, param=None):
        """Activate review widget."""
        #self.review_controller().new_question()
        pass

    def enable_edit_current_card(self, enabled):
        """Enable or disable 'edit card' button."""

        self.w_tree.get_widget("review_toolbar_edit_card_button"). \
            set_sensitive(enabled)
        
    def enable_delete_current_card(self, enabled):
        """Enable or disable 'delete card' button."""

        self.w_tree.get_widget("review_toolbar_delete_card_button"). \
            set_sensitive(enabled)
        
    def set_question(self, text):
        """Set question."""

        self.next_is_image_card = False
        if "sound src=" in text:
            self.sndtext = text
            self.question_container.hide()
            self.sound_container.set_size_request( \
                self.container_width, NORMAL_CONTAINER_HEIGHT)
            self.sound_container.show()
            self.sound_button.set_active(True)
            self.main_widget().start_playing(self.sndtext, self)
        else:
            self.sound_container.hide()            
            if "img src=" in text:
                self.next_is_image_card = True
                self.question_container.set_size_request( \
                    self.container_width, LARGE_CONTAINER_HEIGHT)
            else:
                self.question_container.set_size_request( \
                    self.container_width, 16)
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
            self.renderer.update_show_button( \
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
    def preview_sound_in_review_cb(self, widget):
        """Play/stop listening."""

        if widget.get_active():
            self.main_widget().start_playing(self.sndtext, self)
        else:
            self.main_widget().stop_playing()

    def review_to_main_menu_cb(self, widget):
        """Return to main menu."""

        self.main_widget().stop_playing()
        self.main_widget().activate_mode("menu")

    def get_answer_cb(self, widget, event):
        """Hook for showing a right answer."""

        self.review_controller().show_answer()

    def delete_card_cb(self, widget):
        """Hook for delete card."""

        self.main_widget().stop_playing()
        self.controller().delete_current_fact()

    def edit_card_cb(self, widget):
        """Hook for edit card."""

        self.controller().edit_current_card()

    def grade_cb(self, widget):
        """Call grade of answer."""

        self.main_widget().stop_playing()
        self.review_controller().grade_answer(int(widget.name[-1]))


# Local Variables:
# mode: python
# py-indent-offset: 4
# indent-tabs-mode nil
# tab-width 4
# End:
