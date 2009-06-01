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
Hildon UI
"""

import gettext

from mnemosyne.libmnemosyne.component_manager import database, scheduler, \
        config, ui_controller_review, ui_controller_main
from mnemosyne.libmnemosyne.ui_controller_review import UiControllerReview
from pomni.hildon_ui import HildonBaseController


_ = gettext.gettext


class HildonUiControllerReview(HildonBaseController, UiControllerReview):
    """ Hildon Review controller """

    def __init__(self, w_tree):
        """ Initialization items of review window. """

        HildonBaseController.__init__(self, w_tree)
        UiControllerReview.__init__(self)
        
        signals = ["get_answer", "grade", "delete_card", "edit_card"]

        self.w_tree.signal_autoconnect(\
            {"review_to_main_menu": self.to_main_menu_cb})
        self.w_tree.signal_autoconnect(\
            dict([(sig, getattr(self, sig + "_cb")) for sig in signals]))

        self.grade = 0
        self.card = None

    def activate(self):
        """ Start new review window. """

        self.switcher.set_current_page(self.review)
        self.new_question()

    # UiControllerReview API
    def update_dialog(self, redraw_all=True):
        """ This is part of UiControllerReview API. """

        pass

    def new_question(self, learn_ahead=False):
        """ Create new question """
        pass


    def show_answer(self):
        """ Show answer in review window """
        pass


    def grade_answer(self, grade):
        """ Grade the answer. """

        scheduler().process_answer(self.card, grade)
        self.new_question()

    # Glade callbacks

    def get_answer_cb(self, widget):
        """ Hook for showing a right answer. """

        self.show_answer()

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

        self.grade_answer(int(widget.name[-1]))

    def clear(self):
        """ Unknown """

        self.card = None


class EternalControllerReview(HildonUiControllerReview):
    """ Eternal UI review controller """

    def new_question(self, learn_ahead=False):
        """ Show new question. Make get_answer_box visible. """

        if not database().card_count():
            ui_controller_main().widget.information_box(\
                _("Database is empty!"), "OK")
            self.button_getanswer.set_sensitive(False)
            return

        self.card = scheduler().get_new_question(learn_ahead)
        if self.card:
            document = getattr(self,'question_text').document
            document.clear()
            document.open_stream('text/html')
            # Adapting for html
            question_text = self.card.question()
            if question_text.startswith('<html>'):
                font_size = config()['font_size']
                question_text = question_text.replace('*{font-size:30px;}',
                 '*{font-size:%spx;}' % font_size)
            document.write_stream(question_text)
            document.close_stream()
        else:
            if not ui_controller_main().widget.question_box(
                  _("Learn ahead of schedule?"), _("No"), _("Yes"), ""):
                self.new_question(True)
            else:
                ui_controller_main().widget.information_box(\
                    _("Finished!"), "OK")
                self.button_getanswer.set_sensitive(False)
                return

        for widget in [getattr(self, "grade%i" % num) for num in range(6)]:
            widget.set_sensitive(False)
            
        self.button_getanswer.set_sensitive(True)
        self.get_answer_box.set_property('visible', True)
        self.grades.set_property('visible', False)
        self.answer_box.set_property('visible', False)

    def show_answer(self):
        """ Show answer. Make grades and answer_box visible. """

        for widget in [getattr(self, "grade%i" % num) for num in range(6)]:
            widget.set_sensitive(True)                   
        self.button_getanswer.set_sensitive(True)
        
        answer_text = self.card.answer()
        document = getattr(self,'answer_text').document
        document.clear()
        document.open_stream('text/html')
        if answer_text.startswith('<html>'):
            font_size = config()['font_size']
            answer_text = answer_text.replace('*{font-size:30px;}',
                             '*{font-size:%spx;}' % font_size)
        document.write_stream(answer_text)
        document.close_stream()
        
        self.get_answer_box.set_property('visible', False)
        self.grades.set_property('visible', True)
        self.answer_box.set_property('visible', True)



class RainbowControllerReview(HildonUiControllerReview):
    """ Rainbow UI review controller """

    def new_question(self, learn_ahead=False):
        """ Show new question. """

        self.show_answer("<html><p align=center style='margin-top:35px; \
            font-size:16;'>Press to get answer</p></html>")            
        if not database().card_count():
            ui_controller_main().widget.information_box(\
                _("Database is empty!"), "OK")
            self.answer_viewport.set_sensitive(False)
            self.grades_table.set_sensitive(False)
            return
            
        self.card = scheduler().get_new_question(learn_ahead)
        
        if self.card:
            document = getattr(self,'question_text').document
            document.clear()
            document.open_stream('text/html')
            # Adapting for html
            question_text = self.card.question()
            if question_text.startswith('<html>'):
                font_size = config()['font_size']
                question_text = question_text.replace('*{font-size:30px;}',
                 '*{font-size:%spx;}' % font_size)
            document.write_stream(question_text)
            document.close_stream()
        else:
            if not ui_controller_main().widget.question_box(
                  _("Learn ahead of schedule?"), _("No"), _("Yes"), ""):
                self.new_question(True)
            else:
                ui_controller_main().widget.information_box(\
                    _("Finished!"), "OK")
                self.answer_viewport.set_sensitive(False)
                self.grades_table.set_sensitive(False)
                return        
                
        self.grades_table.set_sensitive(False)

    def show_answer(self, text=None):
        """ Show answer """
        
        self.answer_viewport.set_sensitive(True)
        self.grades_table.set_sensitive(True)
        
        if not text:
            answer_text = self.card.answer()
        else:
            answer_text = text
        document = getattr(self,'answer_text').document
        document.clear()
        document.open_stream('text/html')
        if answer_text.startswith('<html>'):
            font_size = config()['font_size']
            answer_text = answer_text.replace('*{font-size:30px;}',
                             '*{font-size:%spx;}' % font_size)
        document.write_stream(answer_text)
        document.close_stream()


# Local Variables:
# mode: python
# py-indent-offset: 4
# indent-tabs-mode nil
# tab-width 4
# End:
