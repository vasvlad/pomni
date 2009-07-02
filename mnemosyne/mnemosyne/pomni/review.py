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

class RainbowReviewWidget(ReviewWidget):
    """Rainbow theme: Review Widget."""

    def __init__(self, component_manager):
        ReviewWidget.__init__(self, component_manager)
        self.menu = 0
        self.switcher = self.main_widget().switcher
        self.w_tree = self.main_widget().w_tree
        self.w_tree.signal_autoconnect(\
            dict([(sig, getattr(self, sig + "_cb")) \
                for sig in ["review_to_main_menu", "get_answer", 
                    "grade", "delete_card", "edit_card"]]))

    def activate(self):
        """Activate review widget."""
        self.ui_controller_review().new_question()

    def enable_edit_current_card(self, enabled):
        print 'enable_edit_current_card'
        
    def enable_delete_current_card(self, enabled):
        print 'enable_delete_current_card'
        
    def enable_edit_deck(self, enable): 
        print 'enable_edit_deck', enable
        
    def question_box_visible(self, visible):
        print 'question_box_visible', visible
        
    def answer_box_visible(self, visible):
        print 'answer_box_visible', visible
        
    def set_question_label(self, text):
        print 'set_question_label', text
        
    def set_question(self, text):
        print 'set_question', text
        document = self.w_tree.get_widget("question_text").document
        document.clear()
        document.open_stream('text/html')
        # Adapting for html
        if text.startswith('<html>'):
            font_size = self.config()['font_size']
            text = text.replace('*{font-size:30px;}',
                 '*{font-size:%spx;}' % font_size)
        document.write_stream(text)
        document.close_stream()

    def set_answer(self, text):
        print 'set_answer', text
        document = self.w_tree.get_widget('answer_text').document
        document.clear()
        document.open_stream('text/html')
        if text.startswith('<html>'):
            font_size = self.config()['font_size']
            text = text.replace('*{font-size:30px;}',
                             '*{font-size:%spx;}' % font_size)
        document.write_stream(text)
        document.close_stream()

        
    def clear_question(self): 
        print 'clear_question'
        
    def clear_answer(self): 
        print 'clear_answer'

    def update_show_button(self, text, default, enabled): 
        print 'update_show_button', text, default, enabled
        self.w_tree.get_widget("answer_viewport").set_sensitive(enabled)
        if enabled:
            html = "<html><p align=center style='margin-top:35px; \
                font-size:16;'>Press to %s</p></html>" % text
            document = self.w_tree.get_widget("answer_text").document
            document.clear()
            document.open_stream('text/html')
            font_size = self.config()['font_size']
            html = html.replace('*{font-size:30px;}',
                      '*{font-size:%spx;}' % font_size)
            document.write_stream(html)
            document.close_stream()


    def enable_grades(self, enabled): 
        print 'enable_grades', enabled
        self.w_tree.get_widget("grades_table").set_sensitive(enabled)

    def set_default_grade(self, grade):
        print 'set_default_grade', grade
        
    def set_grades_title(self, text): 
        print 'set_grades_title', text
            
    def set_grade_text(self, grade, text): 
        print 'set_grade_text', text
            
    def set_grade_tooltip(self, grade, text): 
        print 'set_grade_tooltip', grade, text

    def update_status_bar(self, message=None):
        print 'update_status_bar', message

    # callbacks
    def review_to_main_menu_cb(self, widget):
        """Return to main menu."""
        self.switcher.set_current_page(self.menu)

    def get_answer_cb(self, widget):
        """ Hook for showing a right answer. """
        print 'get_answer_cb'
        self.ui_controller_review().show_answer()

    def delete_card_cb(self, widget):
        """ Hook for delete card. """

        # Delete card
        if self.card and self.card.fact:
            ui_controller_main().delete_current_fact()

    def edit_card_cb(self, widget):
        """ Hook for edit card. """

        # Edit card
        if self.card and self.card.fact:
            ui_controller_main().edit_current_card()

    def grade_cb(self, widget):
        """ Call grade of answer. """

        print 'grade_cb', int(widget.name[-1])
        self.ui_controller_review().grade_answer(int(widget.name[-1]))



# Local Variables:
# mode: python
# py-indent-offset: 4
# indent-tabs-mode nil
# tab-width 4
# End:
