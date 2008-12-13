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
import gtk
from gtk import glade
from os.path import basename

from mnemosyne.libmnemosyne.component_manager import database, scheduler, \
        ui_controller_review, config, ui_controller_main
from mnemosyne.libmnemosyne.ui_controller_review import UiControllerReview

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
        self.grade = 0
        self.w_tree = None
        self.window = None
        self.question = None
        self.answer = None
        self.eventbox_numeral = []
        self.fullscreen = False
        self.notebook_windows = None
        
        # draft and smile
        self.estimate_box = None
        self.answer_box = None
        self.eventbox_show_answer = None

    def start(self, w_tree):
        """ Start new review window """

        # For common design
        self.notebook_windows = w_tree.get_widget("notebook_windows")

        # Switch to Page review
        self.notebook_windows.set_current_page(1)
        self.window = w_tree.get_widget("ReviewWindow")
        self.question = w_tree.get_widget("question")
        self.answer = w_tree.get_widget("answer")
        self.eventbox_numeral = \
            [w_tree.get_widget("eventbox_numeral_%i" % i) for i in range(6)]

        # Connect to signals
        w_tree.signal_autoconnect({
           "on_eventbox_numeral0_button_press_event": self.numeral_pressed,
           "on_eventbox_numeral1_button_press_event": self.numeral_pressed,
           "on_eventbox_numeral2_button_press_event": self.numeral_pressed,
           "on_eventbox_numeral3_button_press_event": self.numeral_pressed,
           "on_eventbox_numeral4_button_press_event": self.numeral_pressed,
           "on_eventbox_numeral5_button_press_event": self.numeral_pressed,
           "on_eventbox_quit_button_press_event": self.quit_button,
           "on_exit_clicked" : self.quit})

        self.w_tree = w_tree

        self.eventbox_show_answer = \
             self.w_tree.get_widget("eventbox_show_answer")
        # Connect to various signals
        self.w_tree.signal_autoconnect(
            {"on_eventbox_show_answer_button_press_event": 
             self.open_card_clicked})

        self.estimate_box = self.w_tree.get_widget("estimate_box")
        self.answer_box = self.w_tree.get_widget("answer_box")

        # Begin the review window from a new question
        self.new_question()

    def update_dialog(self):
        """ This is part of UiControllerReview API """
        print "Update dialog"

    def show_answer(self):
        """ Show answer in review window """

        self.answer.set_text(self.card.answer())
        for eventbox in self.eventbox_numeral:
            eventbox.set_sensitive(True)
        self.eventbox_show_answer.set_sensitive(False)

    def open_card_clicked(self, widget, event):
        """ Hook for showing a right answer """

        self.show_answer()

    def numeral_pressed(self, widget, event):
        """ Call grade of answer """

        self.grade_answer(self.eventbox_numeral.index(widget))

    def theme_new_question(self):
        """ Visible and Unvisible some items of review windows """

        for eventbox in self.eventbox_numeral:
            eventbox.set_sensitive(False)
        self.eventbox_show_answer.set_sensitive(True)

    def new_question(self):
        """ Create new question """

        if not database().card_count():
            raise HildonUiControllerException(_("Database is empty"))
        
        card = scheduler().get_new_question(False)

        if card != None:
            self.question.set_text(card.question())
            self.answer.set_text("")
            self.theme_new_question()
        else:
            # FIXME
#           value = raw_input(_("Learn ahead of schedule" + "? (y/N)"))
            self.new_question(True)
            self.question.set_text(card.question())
            self.answer.set_text("")
            self.theme_new_question()

        self.card = card

    def grade_answer(self, grade):
        """ Grade the answer """

        scheduler().process_answer(self.card, grade)
        self.new_question()

    def on_key_press(self, widget, event, *args):
        """ Key pressed """
        if event.keyval == gtk.keysyms.F6: 
            # The "Full screen" hardware key has been pressed 
            if self.fullscreen:
                self.window.unfullscreen()
            else:
                self.window.fullscreen()

    def window_state_event(self, widget, event):
        """ Checking window state """

        self.fullscreen = bool(event.new_window_state & \
            gtk.gdk.WINDOW_STATE_FULLSCREEN)

    def quit(self, widget):
        """ Close review window """

    	#Switch to Menu page
        self.notebook_windows.set_current_page(0)

    def quit_button(self, widget, event):
        """ If pressed quit button then close the window """
        
        self.quit(widget)


class MainWindow:
    """ GUI - Hildon """

    def __init__(self, mode):

        theme_path = config()["theme_path"]
        gtk.rc_parse(os.path.join(theme_path,"rcfile"))
        self.w_tree = gtk.glade.XML(os.path.join(theme_path,
                                                 "window.glade"))
        self.w_tree.signal_autoconnect({
                "on_review_clicked": self.review_clicked,
                "on_input_clicked" : self.input_clicked,
                "on_configure_clicked" : self.configure_clicked,
                "on_MainWindow_key_press_event" : self.on_key_press,
                "on_MainWindow_window_state_event": self.window_state_event,
                "on_exit_clicked" : self.quit})
        self.window = self.w_tree.get_widget("MainWindow")

        self.fullscreen = False

        # FIXME
        if mode == "review":
            ui_controller_review().start(self.w_tree)

    def review_clicked(self, widget):
        """ Open Review Window """

        ui_controller_review().start(self.w_tree)

    def input_clicked(self, widget):
        """ Open Input Window """

        print "button Input clicked"

    def configure_clicked(self, widget):
        """ Open configure window """

        print "button Configure clicked"

    def quit(self, widget):
        """ Quit from application """

        gtk.main_quit()

    def on_key_press(self, widget, event, *args):
        """ Key pressed """

        if event.keyval == gtk.keysyms.F6:
            # The "Full screen" hardware key has been pressed 
            if self.fullscreen:
                self.window.unfullscreen ()
            else:
                self.window.fullscreen ()

    def window_state_event(self, widget, event):
        """ Checking window state """

        self.fullscreen = bool(event.new_window_state & \
            gtk.gdk.WINDOW_STATE_FULLSCREEN)


class HildonUI():
    """ Hildon UI. Upper-level class """

    def __init__(self):
        ui_controller_main().widget = self

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
