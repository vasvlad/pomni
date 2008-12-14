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
import gtk.glade
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

    # page's indexes in switcher
    main_menu, review, input = range(3)

    # widgets
    wnames = ("window", "switcher", "get_answer", "question", "answer",
              "grades", "get_answer_box", "answer_box",
              "grade0", "grade1", "grade2", "grade3", "grade4", "grade5")

    # signals
    signals = ("get_answer", "grade", "to_main_menu", "window_state", 
               "window_keypress")

    def __init__(self):
        """ Initialization items of review window """

        UiControllerReview.__init__(self, name="Hildon UI Controller")

        self.title = _("Mnemosyne") + " - " + \
            os.path.splitext(basename(config()["path"]))[0]

        self.grade = 0
        self.card = None
        self.fullscreen = False
        self.widgets = []

    def start(self, w_tree):
        """ Start new review window """

        # store widgets objects
        self.widgets = dict([(wname, w_tree.get_widget(wname)) \
                            for wname in self.wnames])

        # switch to Page review
        # switcher - window with tabs. Each tab is for
        # different mode (main_menu, review, conf, input, etc)
        self.widgets["switcher"].set_current_page(self.review)

        # connect signals to methods
        w_tree.signal_autoconnect(dict([(sig, getattr(self, sig + "_cb")) \
            for sig in self.signals]))

        # Begin the review window from a new question
        self.new_question()

    # UiControllerReview API
    
    def update_dialog(self):
        """ This is part of UiControllerReview API """
        pass

    def new_question(self):
        """ Create new question """

        def theme_new_question(self):
            """ Visible and Unvisible some items of review windows """

            for grade in range(6):
                self.widgets["grade%i" % grade].set_sensitive(False)
            self.widgets["get_answer"].set_sensitive(True)

            # eternal
            self.widgets["grades"].set_property('visible', False)
            self.widgets["get_answer_box"].set_property('visible', True)
            self.widgets["answer_box"].set_property('visible', False)

        if not database().card_count():
            raise HildonUiControllerException(_("Database is empty"))

        card = scheduler().get_new_question(False)

        if card != None:
            self.widgets["question"].set_text(card.question())
            self.widgets["answer"].set_text("")
            theme_new_question(self)
        else:
            # FIXME
#           value = raw_input(_("Learn ahead of schedule" + "? (y/N)"))
            self.new_question(True)
            self.widgets["question"].set_text(card.question())
            self.widgets["answer"].set_text("")
            theme_new_question(self)

        self.card = card

    def show_answer(self):
        """ Show answer in review window """

        self.widgets["answer"].set_text(self.card.answer())
        for widget in [self.widgets["grade%i" % num] for num in range(6)]:
            widget.set_sensitive(True)
        self.widgets["get_answer"].set_sensitive(False)

        # eternal
        self.widgets["get_answer_box"].set_property('visible', False)
        self.widget["grades"].set_property('visible', True)
        self.widget["answer_box"].set_property('visible', True)
        self.widget["answer"].set_text(self.card.answer())

    def grade_answer(self, grade):
        """ Grade the answer """

        scheduler().process_answer(self.card, grade)
        self.new_question()

    # Glade callbacks
    def get_answer_cb(self, widget, event):
        """ Hook for showing a right answer """

        self.show_answer()

    def grade_cb(self, widget, event):
        """ Call grade of answer """

        print "grade_cb", widget, event
        self.grade_answer()

    def to_main_menu_cb(self, widget):
        """ Return to main menu """

        self.widgets["switcher"].set_current_page(self.main_menu)

    def exit_cb(self, widget):
        """ If pressed quit button then close the window """

        gtk.main_quit()

    def window_keypress_cb(self, widget, event, *args):
        """ Key pressed """
        if event.keyval == gtk.keysyms.F6: 
            # The "Full screen" hardware key has been pressed 
            if self.fullscreen:
                self.widgets["window"].unfullscreen()
            else:
                self.widgets["window"].fullscreen()

    def window_state_cb(self, widget, event):
        """ Checking window state """

        self.fullscreen = bool(event.new_window_state & \
            gtk.gdk.WINDOW_STATE_FULLSCREEN)


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
