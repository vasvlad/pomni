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

import os
import gettext
import gtk
import gtk.glade
from os.path import splitext, basename

from mnemosyne.libmnemosyne.component_manager import database, scheduler, \
        ui_controller_review, config, ui_controller_main #, ui_controller_input
from mnemosyne.libmnemosyne.ui_controller_review import UiControllerReview
from mnemosyne.libmnemosyne.ui_controller_main import UiControllerMain

_ = gettext.gettext


class HildonUiControllerException(Exception):
    """ Exception hook """

    def __init__(self, w_tree, exception):
        """ Show Warning Window """

        self.warning_window = w_tree.get_widget("warningwindow")
        warning_label = w_tree.get_widget("label_warning")
        self.signals = ["close"]
        # connect signals to methods
        w_tree.signal_autoconnect(dict([(sig, getattr(self, sig + "_cb")) \
            for sig in self.signals]))
        # Show warning text
        warning_label.set_text(exception)
        self.warning_window.show()

        Exception.__init__(self)

    def __getattr__(self, name):
        """ Lazy get widget as an attribute """

        widget = self.w_tree.get_widget(name)
        if widget:
            return widget
        raise AttributeError()

    def close_cb(self, widget, event):
        """ Close Warning Window """
        self.warning_window.hide()


class HildonBaseUi():
    """ Base Hildon UI functionality """

    # page's indexes in switcher
    main_menu, review, input = range(3)

    def __init__(self, signals):

        self.signals = ["exit", "to_main_menu", "window_state",
                        "window_keypress"]
        if signals:
            self.signals.extend(signals)

        self.w_tree = None
        self.fullscreen = False

    def __getattr__(self, name):
        """ Lazy get widget as an attribute """

        widget = self.w_tree.get_widget(name)
        if widget:
            return widget
        raise AttributeError()

    def start(self, w_tree):
        """ Init w_tree, connect callbacks to signals """

        self.w_tree = w_tree

        # connect signals to methods
        w_tree.signal_autoconnect(dict([(sig, getattr(self, sig + "_cb")) \
            for sig in self.signals]))

    # Callbacks

    @staticmethod
    def exit_cb(widget):
        """ If pressed quit button then close the window """

        gtk.main_quit()

    def to_main_menu_cb(self, widget, event):
        """ Return to main menu """

        self.switcher.set_current_page(self.main_menu)

    def window_keypress_cb(self, widget, event, *args):
        """ Key pressed """
        if event.keyval == gtk.keysyms.F6:
            # The "Full screen" hardware key has been pressed
            if self.fullscreen:
                self.window.unfullscreen()
            else:
                self.window.fullscreen()

    def window_state_cb(self, widget, event):
        """ Checking window state """

        self.fullscreen = bool(event.new_window_state & \
            gtk.gdk.WINDOW_STATE_FULLSCREEN)


class HildonUiControllerReview(HildonBaseUi, UiControllerReview):
    """ Hildon Review controller """

    def __init__(self):
        """ Initialization items of review window """

        HildonBaseUi.__init__(self, signals=["get_answer", "grade"])
        UiControllerReview.__init__(self, name="Hildon UI Review Controller")

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

    def update_dialog(self):
        """ This is part of UiControllerReview API """
        pass

    def new_question(self, learn_ahead=False):
        """ Create new question """

        if not database().card_count():
            raise HildonUiControllerException(self.w_tree, \
                _("Database is empty"))

        card = scheduler().get_new_question(learn_ahead)

        if card:
            self.question.set_text(card.question())
        else:
            # FIXME value = raw_input(_("Learn ahead of schedule" + "? (y/N)"))
            self.new_question(True)
            #self.question.set_text(card.question())

        self.answer.set_text("")
        for widget in [getattr(self, "grade%i" % num) for num in range(6)]:
            widget.set_sensitive(False)
        self.get_answer.set_sensitive(True)
        self.card = card

    def show_answer(self):
        """ Show answer in review window """

        self.answer.set_text(self.card.answer())
        for widget in [getattr(self, "grade%i" % num) for num in range(6)]:
            widget.set_sensitive(True)
        self.get_answer.set_sensitive(False)
        self.answer.set_text(self.card.answer())

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

        self.grade_answer(int(widget.name[-1]))

    def clear(self):
        """ Unknown """

        self.card = None


#class HildonUiControllerInput(HildonBaseUi):
#    """ Hildon Review controller """
#
#    def __init__(self):
#        """ Initialization items of review window """
#
#        HildonBaseUi.__init__(self, signals=[])
#
#        self.title = _("Mnemosyne") + " - " + \
#            splitext(basename(config()["path"]))[0]
#
#
#    def start(self, w_tree):
#        """ Start new review window """
#
#        HildonBaseUi.start(self, w_tree)
#
#        # switch to Page review
#        # switcher - window with tabs. Each tab is for
#        # different mode (main_menu, review, conf, input, etc)
#        self.switcher.set_current_page(self.input)


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


class HildonUiControllerMain(HildonBaseUi, UiControllerMain):
    """ Hidon Main Controller  """

    def __init__(self, extrasignals=None):
        """ Iniitialization """

        signals = ["review", "input", "configure"]
        if extrasignals:
            signals.extend(extrasignals)

        HildonBaseUi.__init__(self, signals)
        UiControllerMain.__init__(self, name="Hildon UI Main Controller")

        ui_controller_main().widget = self

    def create_new_cards(self, fact_data, card_type, grade, cat_names):
        """ Create new cards. Mnenosyne API """

        print 'Creating new cards', fact_data, card_type, grade, cat_names

    def add_cards(self):
        """ Add cards.Mnenosyne API """

        print 'Adding new cards'

    # Callbacks

    def review_cb(self, widget):
        """ Start Review """

        ui_controller_review().start(self.w_tree)

    def input_cb(self, widget):
        """ Start Input """

        ui_controller_input().start(self.w_tree)

    @staticmethod
    def configure_cb(widget):
        """ Start configure mode """

        raise NotImplemented(widget)

    def edit_current_card(self):
        """ Not Implemented Yet """

        pass

    def update_related_cards(self, fact, new_fact_data, new_card_type, \
                             new_cat_names):
        """ Not Implemented """

        pass

    def file_new(self):
        """ Not Implemented Yet """

        pass

    def file_open(self):
        """ Not Implemented Yet """

        pass

    def file_save(self):
        """ Not Implemented Yet """

        pass

    def file_save_as(self):
        """ Not Implemented Yet """

        pass


class EternalControllerMain(HildonUiControllerMain):
    """ Eternal UI Main Controller """

    def __init__(self):
        """ Added spliter widget to class """

        self.base = HildonUiControllerMain
        self.base.__init__(self, ["size_allocate"])
        self.spliter_trigger = True

    def start(self, w_tree):
        """ Start base class """
        HildonBaseUi.start(self, w_tree)

    def size_allocate_cb(self, widget, user_data):
        """ Checking window size """

        if (self.switcher.get_current_page() == self.review):
            if (self.spliter_trigger):
                # Set Spliter (GtkVpan) to pseudo medium
                self.spliter_trigger = False
                pseudo_medium = (widget.allocation.height - 70)/2 - 20
                self.spliter.set_property('position', pseudo_medium)
            else:
                self.spliter_trigger = True


class SmileControllerMain(HildonUiControllerMain):
    """ Smile UI Main Controller """

    pass


class SmileControllerReview(HildonUiControllerReview):
    """ Smile UI Review Controller """

    pass


class DraftControllerMain(HildonUiControllerMain):
    """ Draft UI Main Controller """

    pass


class DraftControllerReview(HildonUiControllerReview):
    """ Draft UI Review Controller """

    pass

#class EternalControllerInput(HildonUiControllerInput):
#    """ Eteranl UI Input Controller """
#
#    pass


class HildonUI():
    """ Hildon UI """

    def __init__(self):
        """ Load theme's glade file """

        theme_path = config()["theme_path"]
        gtk.rc_parse(os.path.join(theme_path, "rcfile"))
        self.w_tree = gtk.glade.XML(os.path.join(theme_path, "window.glade"))

        # Set unvisible tabs of switcher
        switcher = self.w_tree.get_widget("switcher")
        switcher.set_property('show_tabs', False)

    def start(self, mode):
        """ Start UI  """

        globals()["ui_controller_%s" % mode]().start(self.w_tree)
        gtk.main()


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
