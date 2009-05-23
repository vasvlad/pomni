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
import gtkhtml2

from mnemosyne.libmnemosyne.component_manager import config, \
    ui_controller_main, database

_ = gettext.gettext


class HildonUiControllerException(Exception):
    """ Exception hook """

    def __init__(self, w_tree, exception):
        """ Show Warning Window """

        dialog = w_tree.get_widget("information_dialog")
        w_tree.get_widget("information_dialog_label").set_text(\
            '\n' + "  " + exception + "  " + '\n')
        dialog.run()
        dialog.hide()

        Exception.__init__(self)



class HildonBaseUi():
    """ Base Hildon UI functionality """

    # page's indexes in switcher
    main_menu, review, input, config = range(4)

    def __init__(self, signals):

        self.signals = ["to_main_menu"]

        if signals:
            self.signals.extend(signals)

        self.w_tree = None
        self.starting = False

    def __getattr__(self, name):
        """ Lazy get widget as an attribute """

        widget = self.w_tree.get_widget(name)
        if widget:
            return widget
        raise AttributeError()

    def start(self, w_tree):
        """ Init w_tree, connect callbacks to signals """

        if not self.w_tree:
            self.w_tree = w_tree

            # connect signals to methods
            w_tree.signal_autoconnect(dict([(sig, getattr(self, sig + "_cb")) \
                for sig in self.signals]))


    def to_main_menu_cb(self, widget):
        """ Return to main menu """

        self.switcher.set_current_page(self.main_menu)



class HildonUI():
    """ Hildon UI """

    def __init__(self, controllers):

        def gen_callback(mode):
            """Generate callback for mode."""

            def callback(widget, event = None):
                """Callback function."""
                self.controllers[mode].start(self.w_tree)
            return callback

        ui_controller_main().widget = self
        theme_path = config()["theme_path"]
        gtk.rc_parse(os.path.join(theme_path, "rcfile"))
        gtk.glade.set_custom_handler(self.custom_handler)
        self.w_tree = gtk.glade.XML(os.path.join(theme_path, "window.glade"))

        # Set unvisible tabs of switcher
        switcher = self.w_tree.get_widget("switcher")
        switcher.set_property('show_tabs', False)
        self.window = self.w_tree.get_widget("window")
        self.window.connect('delete_event', self.exit_cb)

        self.question_flag = False
        # fullscreen mode
        if config()['fullscreen']:
            self.window.fullscreen()
            self.fullscreen = True
        else:
            self.fullscreen = False

        # Generate callbacks for modes
        self.controllers = controllers
        signals = ["review", "input", "configure"]
        for signal in signals:
            setattr(self, signal + '_cb', gen_callback(signal))

        self.signals = ["exit", "window_state", "window_keypress"] + signals

        # connect signals to methods
        self.w_tree.signal_autoconnect(dict([(sig, getattr(self, sig + "_cb")) \
            for sig in self.signals]))

    def start(self, mode):
        """ Start UI  """

        self.controllers[mode].start(self.w_tree)
        gtk.main()

    def custom_handler(self, glade, function_name, widget_name, *args):

        """ Hook for custom widgets """

        if glade and widget_name and  hasattr(self, function_name):
            handler = getattr(self, function_name)
            return handler(args)

    # Callbacks

    @staticmethod
    def exit_cb(widget=None):
        """ If pressed quit button then close the window """

        database().unload()
        gtk.main_quit()


    def window_keypress_cb(self, widget, event, *args):
        """ Key pressed """

        if event.keyval == gtk.keysyms.F6:
            # The "Full screen" hardware key has been pressed
            if self.fullscreen:
                self.window.unfullscreen()
                self.fullscreen = False
            else:
                self.window.fullscreen()
                self.fullscreen = True

    def window_state_cb(self, widget, event):
        """ Checking window state """

        self.fullscreen = bool(event.new_window_state & \
            gtk.gdk.WINDOW_STATE_FULLSCREEN)


    @staticmethod
    def create_gtkhtml(args):
        """ Create gtkhtml2 widget """

        view = gtkhtml2.View()
        document = gtkhtml2.Document()
        view.set_document(document)
        view.document = document
        view.show()
        return view

    @staticmethod
    def clear_label(caption):
        """ Remove &-symbol from caption if exists"""
        index = caption.find("&")
        if not index == -1:
            return caption[:index] + caption[index+1:]
        return caption
    
    def information_box(self, message, button_caption):
        """ Create Information message """
        dialog = self.w_tree.get_widget("information_dialog")
        self.w_tree.get_widget("information_dialog_label").set_text(\
            '\n' + "  " + message + "  " + '\n')
        self.w_tree.get_widget("information_dialog_button_ok").set_label(\
            button_caption)
        dialog.run()
        dialog.hide()

    def question_box(self, question, option0, option1, option2):
        """ Create Question message """
        dialog = self.w_tree.get_widget("question_dialog")
        dialog_label = self.w_tree.get_widget("question_dialog_label")
        dialog_label.set_text('\n' + "  " + question + "  " + '\n')
        result = True
        response = dialog.run()
        if response == -8:
            result = False
        dialog.hide()
        return result

    def update_status_bar(self, message=None):
        """ Not Implemented """

        pass

    def run_edit_fact_dialog(self, fact, allow_cancel=True):
        """ Start Edit/Update window """

        self.controllers['input'].start(self.w_tree,fact)


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
