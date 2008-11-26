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

class HildonUiControllerException(Exception): pass

_ = gettext.gettext

class HildonUiControllerReview(UiControllerReview):
    """ GUI - Hildon """

    def __init__(self):
        UiControllerReview.__init__(self, name="Command line UI Controller")
        self.title = _("Mnemosyne") + " - " + basename(config()["path"])[:-4]
        self.gladefn = os.path.join(config()["theme_path"], "window_review.glade")
        self.grade = 0

    def numeral0_pressed(self,widget,event):
        self.grade_answer(0)

    def numeral1_pressed(self,widget,event):
        self.grade_answer(1)

    def numeral2_pressed(self,widget,event):
        self.grade_answer(2)

    def numeral3_pressed(self,widget,event):
        self.grade_answer(3)

    def numeral4_pressed(self,widget,event):
        self.grade_answer(4)

    def numeral5_pressed(self,widget,event):
        self.grade_answer(5)

    def open_card_clicked(self,widget,event):
        self.show_answer()

    def start(self):
        wTree = glade.XML(self.gladefn)
        wTree.signal_autoconnect({"on_eventbox_numeral0_button_press_event": self.numeral0_pressed,
                                  "on_eventbox_numeral1_button_press_event": self.numeral1_pressed,
                                  "on_eventbox_numeral2_button_press_event": self.numeral2_pressed,
                                  "on_eventbox_numeral3_button_press_event": self.numeral3_pressed,
                                  "on_eventbox_numeral4_button_press_event": self.numeral4_pressed,
                                  "on_eventbox_numeral5_button_press_event": self.numeral5_pressed,
                                  "on_eventbox_show_answer_button_press_event": self.open_card_clicked,
                                  "on_exit_clicked" : self.quit})

        self.question = wTree.get_widget("question")
        self.answer = wTree.get_widget("answer")
        self.eventbox_numeral0 = wTree.get_widget("eventbox_numeral_0")
        self.eventbox_numeral1 = wTree.get_widget("eventbox_numeral_1")
        self.eventbox_numeral2 = wTree.get_widget("eventbox_numeral_2")
        self.eventbox_numeral3 = wTree.get_widget("eventbox_numeral_3")
        self.eventbox_numeral4 = wTree.get_widget("eventbox_numeral_4")
        self.eventbox_numeral5 = wTree.get_widget("eventbox_numeral_5")
        self.eventbox_show_answer = wTree.get_widget("eventbox_show_answer")

        self.wTree = wTree

        self.new_question()

    def new_question(self, learn_ahead=False):
        if database().card_count() == 0:
            raise HildonUiControllerException(_("Database is empty"))
        else:
            self.card = scheduler().get_new_question(learn_ahead)
            if self.card != None:
                self.question.set_text(self.card.question())
                self.answer.set_text("")
                self.eventbox_numeral0.set_sensitive(False)
                self.eventbox_numeral1.set_sensitive(False)
                self.eventbox_numeral2.set_sensitive(False)
                self.eventbox_numeral3.set_sensitive(False)
                self.eventbox_numeral4.set_sensitive(False)
                self.eventbox_numeral5.set_sensitive(False)
                self.eventbox_show_answer.set_sensitive(True)
            else:
#                value = raw_input(_("Learn ahead of schedule" + "? (y/N)"))
                self.new_question(learn_ahead=True)

    def show_answer(self):
        self.answer.set_text(self.card.answer())
        self.eventbox_numeral0.set_sensitive(True)
        self.eventbox_numeral1.set_sensitive(True)
        self.eventbox_numeral2.set_sensitive(True)
        self.eventbox_numeral3.set_sensitive(True)
        self.eventbox_numeral4.set_sensitive(True)
        self.eventbox_numeral5.set_sensitive(True)
        self.eventbox_show_answer.set_sensitive(False)

    def grade_answer(self, grade):
        scheduler().process_answer(self.card, grade)
        self.new_question()

    def quit(self,widget):
        raise HildonUiControllerException(_("Exited"))
        self.window.destroy()

class MainWindow:
    """ GUI - Hildon """

    def __init__(self,mode):
       
        theme_path = config()["theme_path"]
        self.wTree=gtk.glade.XML(os.path.join(theme_path, "window_main.glade"))
        self.wTree.signal_autoconnect({"on_review_clicked": self.review_clicked,
                                       "on_input_clicked" : self.input_clicked,
                                       "on_configure_clicked" : self.configure_clicked,
                                       "on_eventbox1_button_press_event" : self.quit,
                                       "on_exit_clicked" : self.quit})
        self.window = self.wTree.get_widget("MainWindow")

        gtk.rc_parse(os.path.join(theme_path,"rcfile"))

        # Fix Me 
        if (mode == 'review'):
            ui_controller_review().start()

    def review_clicked(self,widget):
        print "button Review clicked"
        ui_controller_review().start()

    def input_clicked(self,widget):
        print "button Input clicked"

    def configure_clicked(self,widget):
        print "button Configure clicked"

    def quit(self,widget):
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

    def information_box(self, message, OK_string):
        print message

    def question_box(self, question, option0, option1, option2):
        print question
        print "0", option0
        print "1", option1
        print "2", option2
        answer = raw_input(_("Enter number of answer for select it "))

        return answer

    def start(self, mode):
        app = MainWindow(mode)
        gtk.main()

    def do_quit(self, line):
        """ Quit the program """ 
        return True

    def do_review(self, line):
        """ Review mode """
        ui_controller_review().start()

    def do_input(self, line):
        """ Input mode """
        print("=== Input mode === Not implemented yet")

    def do_conf(self, line):
        """ Configuration mode """
        print "Configuration mode. Not implemented yet"


class HildonReviewWdgt:
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
