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

from os.path import splitext, basename

from mnemosyne.libmnemosyne.component_manager import database, scheduler, \
        config, ui_controller_main
from mnemosyne.libmnemosyne.ui_controller_review import UiControllerReview

from pomni.hildon_ui import HildonBaseUi, HildonUiControllerException

_ = gettext.gettext


class HildonUiControllerReview(HildonBaseUi, UiControllerReview):
    """ Hildon Review controller """

    def __init__(self):
        """ Initialization items of review window """

        HildonBaseUi.__init__(self, signals=["get_answer", \
            "grade", "delete_card"])
        UiControllerReview.__init__(self)

        self.title = _("Mnemosyne") + " - " + \
            splitext(basename(config()["path"]))[0]

        self.grade = 0
        self.card = None


    def start(self, w_tree):
        """ Start new review window """

        HildonBaseUi.start(self, w_tree)


        # switch to Page review
        # switcher - window with tabs. Each tab is for
        # different mode (main_menu, review, conf, input, etc)
        self.switcher.set_current_page(self.review)

        # Begin the review window from a new question
        self.new_question()

    # UiControllerReview API


    def update_dialog(self, redraw_all):
        """ This is part of UiControllerReview API """

        self.new_question()

    def new_question(self, learn_ahead=False):
        """ Create new question """

        if not database().card_count():
            raise HildonUiControllerException(self.w_tree, \
                _("Database is empty"))

        self.card = scheduler().get_new_question(learn_ahead)

        if self.card:
            document = getattr(self,'question_text').document
            #view = getattr(self,'question_text')
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
            if ui_controller_main().widget.question_box(
                  _("Learn ahead of schedule"), _("No"), _("Yes"), ""):
                self.new_question(True)
            else:
                raise HildonUiControllerException(self.w_tree, _("Finished"))

        for widget in [getattr(self, "grade%i" % num) for num in range(6)]:
            widget.set_sensitive(False)
        self.get_answer.set_sensitive(True)

    def show_answer(self):
        """ Show answer in review window """

        for widget in [getattr(self, "grade%i" % num) for num in range(6)]:
            widget.set_sensitive(True)
        self.get_answer.set_sensitive(False)

        #view = getattr(self,'answer_text')
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


    def grade_answer(self, grade):
        """ Grade the answer """

        scheduler().process_answer(self.card, grade)
        self.new_question()

    # Glade callbacks

    def get_answer_cb(self, widget, event):
        """ Hook for showing a right answer """

        self.show_answer()

    @staticmethod
    def delete_card_cb(widget):
        """ Hook for showing a right answer """

        # Create new card
        main = ui_controller_main()
        main.delete_current_fact()

    def grade_cb(self, widget, event):
        """ Call grade of answer """

        self.grade_answer(int(widget.name[-1]))

    def clear(self):
        """ Unknown """

        self.card = None



class EternalControllerReview(HildonUiControllerReview):
    """ Eternal UI review controller """

    def __init__(self):
        self.base = HildonUiControllerReview
        self.base.__init__(self)

    def new_question(self, learn_ahead=False):
        """ Show new question. Make get_answer_box visible """

        self.base.new_question(self, learn_ahead)
        self.get_answer_box.set_property('visible', True)
        self.grades.set_property('visible', False)
        self.answer_box.set_property('visible', False)

    def show_answer(self):
        """ Show answer. Make grades and answer_box visible """

        self.base.show_answer(self)
        self.get_answer_box.set_property('visible', False)
        self.grades.set_property('visible', True)
        self.answer_box.set_property('visible', True)


def _test():
    """ Run doctests
    """
    import doctest
    doctest.testmod()


if __name__ == "__main__":
    _test()


# Local Variables:
# mode: python
# py-indent-offset: 4
# indent-tabs-mode nil
# tab-width 4
# End: