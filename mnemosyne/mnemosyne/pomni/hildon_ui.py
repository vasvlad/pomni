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
Hildon UI
"""

import os
import gettext
from os.path import basename

import gtk
from gtk import glade
try:
    import hildon
    IS_MAEMO = True
except:
    IS_MAEMO = False


from mnemosyne.libmnemosyne.component_manager import database, scheduler, \
        ui_controller_review, config, ui_controller_main, card_types
from mnemosyne.libmnemosyne.ui_controller_review import UiControllerReview
from mnemosyne.libmnemosyne.ui_controllers_review.SM2_controller \
    import SM2Controller

_ = gettext.gettext

class HildonUiControllerException(Exception): 
    """ Exception hook """

    pass

class HildonUiControllerReview(UiControllerReview):
    """ GUI - Hildon """

    def __init__(self):
        """ Initialization items of review window """

        UiControllerReview.__init__(self, name="Hildon UI Controller")
        self.title = _("Mnemosyne") + " - " + basename(config()["path"])[:-4]
        self.gladefn = os.path.join(config()["theme_path"], 
                                            "window_review.glade")
        self.grade = 0
        self.w_tree = None
        self.window = None
        self.question = None
        self.answer = None
        self.eventbox_numeral0 = None
        self.eventbox_numeral1 = None
        self.eventbox_numeral2 = None
        self.eventbox_numeral3 = None
        self.eventbox_numeral4 = None
        self.eventbox_numeral5 = None

    def start(self):
        """ Start new review window """

        # Load the glade form for review window
        self.w_tree = glade.XML(self.gladefn)

        #For common design
        self.window = self.w_tree.get_widget("ReviewWindow")
        self.question = self.w_tree.get_widget("question")
        self.answer = self.w_tree.get_widget("answer")
        self.eventbox_numeral0 = self.w_tree.get_widget("eventbox_numeral_0")
        self.eventbox_numeral1 = self.w_tree.get_widget("eventbox_numeral_1")
        self.eventbox_numeral2 = self.w_tree.get_widget("eventbox_numeral_2")
        self.eventbox_numeral3 = self.w_tree.get_widget("eventbox_numeral_3")
        self.eventbox_numeral4 = self.w_tree.get_widget("eventbox_numeral_4")
        self.eventbox_numeral5 = self.w_tree.get_widget("eventbox_numeral_5")

    def update_dialog(self):
        """ This is part of UiControllerReview API """

        pass


    def show_answer(self):
        """ Show a right answer """

        pass

    def open_card_clicked(self, widget, event):
        """ Hook for showing a right answer """

        if (widget and event):
            self.show_answer()


    def numeral_pressed(self, widget, event):
        """ Call grade of answer """

        if not (widget and event):
            return
        if (widget == self.eventbox_numeral0):
            self.grade_answer(0)
        if (widget == self.eventbox_numeral1):
            self.grade_answer(1)
        if (widget == self.eventbox_numeral2):
            self.grade_answer(2)
        if (widget == self.eventbox_numeral3):
            self.grade_answer(3)
        if (widget == self.eventbox_numeral4):
            self.grade_answer(4)
        if (widget == self.eventbox_numeral5):
            self.grade_answer(5)

    def theme_new_question(self):
        """ Show New question on current theme """
        pass
        
    def new_question(self, learn_ahead = False):
        """ Create new question """

        if database().card_count() == 0:
            raise HildonUiControllerException(_("Database is empty"))
        else:
            self.card = scheduler().get_new_question(learn_ahead)

            if self.card != None:
                self.question.set_text(self.card.question())
                self.answer.set_text("")
                self.theme_new_question()
            else:
                #Fix me
#                value = raw_input(_("Learn ahead of schedule" + "? (y/N)"))
                self.new_question(learn_ahead=True)

    def grade_answer(self, grade):
        """ Grade the answer """

        scheduler().process_answer(self.card, grade)
        self.new_question()

    def quit(self, widget):
        """ Close review window """

        if (widget):
            self.window.destroy()

    def quit_button(self, widget, event):
        """ If pressed quit button then close the window """

        if (widget and event):
            self.quit(widget)



class MainWindow:
    """ GUI - Hildon """

    def __init__(self, mode):

        theme_path = config()["theme_path"]
        self.w_tree = gtk.glade.XML(os.path.join(theme_path,
                                                 "window_main.glade"))
        self.w_tree.signal_autoconnect({
                "on_review_clicked": self.review_clicked,
                "on_input_clicked" : self.input_clicked,
                "on_configure_clicked" : self.configure_clicked,
                "on_eventbox1_button_press_event" : self.quit,
                "on_exit_clicked" : self.quit})
        self.window = self.w_tree.get_widget("MainWindow")
        gtk.rc_parse(os.path.join(theme_path,"rcfile"))

        # Fix Me 
        if (mode == 'review'):
            ui_controller_review().start()

    def review_clicked(self, widget):
        """ Open Review Window """

        if (widget):
            ui_controller_review().start()

    def input_clicked(self, widget):
        """ Open Input Window """

        if (widget):
            print "button Input clicked"

    def configure_clicked(self, widget):
        """ Open configure window """

        if (widget):
            print "button Configure clicked"

    def quit(self, widget):
        """ Quit from application """

        if (widget):
            gtk.main_quit()

class HildonUI():
    """ Hildon UI. Upper-level class """

    def __init__(self, model):
        ui_controller_main().widget = self
        self.model = model
        model.register(self)

    def update(self, model):
        """ This method is part of Observer pattern
            it's called by observable(Model in our case) to notify
            about its change
        """
        pass

    def information_box(self, message, ok_string):
        """ Output messsage """

        print message

    def question_box(self, question, option0, option1, option2):
        """ Show question """

        print question
        print "0", option0
        print "1", option1
        print "2", option2
        answer = raw_input(_("Enter number of answer for select it "))

        return answer

    def start(self, mode):
        """ Start GUI application """

        MainWindow(mode)
        gtk.main()

    def do_quit(self, line):
        """ Quit from the program """

        print line
        return True

    def do_review(self, line):
        """ Review mode """

        ui_controller_review().start()

    def do_input(self, line):
        """ Input mode """

        print("=== Input mode === Not implemented yet")
        print line

    def do_conf(self, line):
        """ Configuration mode """

        print "Configuration mode. Not implemented yet"
        print line


class HildonReviewWdgt:
    """ HildonReviewWdgt Now I do not know, this class what for is necessary"""

    def __init__(self):
        pass

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
