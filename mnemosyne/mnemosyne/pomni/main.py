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
Hildon UI. Main Widget.
"""

import os
import gettext
import gtk
import gtk.glade
import gtkhtml2
import urllib
import urlparse

from mnemosyne.libmnemosyne.ui_components.main_widget import MainWidget

_ = gettext.gettext

htmlOpener = urllib.FancyURLopener()

class HildonMainWidget(MainWidget):
    """Hildon main widget."""

    menu, review, input, configuration = range(4)

    def activate(self, param=None):
        """Basic UI setup. 
           Load theme glade file, assign gtk window callbacks.
        """

        self.widgets = {}

        # Load the glade file for current theme
        theme_path = self.config()["theme_path"]
        self.theme = theme_path.split("/")[-1]
        gtk.rc_parse(os.path.join(theme_path, "rcfile"))
        gtk.glade.set_custom_handler(self.custom_handler)
        w_tree = gtk.glade.XML(os.path.join(theme_path, "window.glade"))

        self.switcher = w_tree.get_widget("switcher")
        self.window = w_tree.get_widget("window")

        self.question_flag = False
        # fullscreen mode
        if self.config()['fullscreen']:
            self.window.fullscreen()
            self.fullscreen = True
        else:
            self.fullscreen = False

        # connect signals to methods
        self.window.connect("delete_event", self.exit_)
        w_tree.signal_autoconnect(dict([(sig, getattr(self, sig + "_cb")) \
            for sig in ("window_state", "window_keypress")]))

        self.question_dialog = w_tree.get_widget("question_dialog")
        self.information_dialog = w_tree.get_widget("information_dialog")
        self.question_dialog_label = w_tree.get_widget("question_dialog_label")
        self.information_dialog_label = w_tree.get_widget(\
            "information_dialog_label")

        self.w_tree = w_tree
        self.soundmanager = None

    def activate_mode(self, mode, param=None):
        """Activate mode in lazy way."""

        self.switcher.set_current_page(getattr(self, mode))
        widget = self.widgets.get(mode, None)
        if not widget: # lazy widget creation
            cname = self.theme.capitalize() + '%sWidget' % mode.capitalize()
            module = __import__("pomni.%s" % mode, globals(),
                                locals(), [cname])
            w_class = getattr(module, cname)
            if mode == "review":
                self.component_manager.register(w_class)
                self.review_controller().reset()
                widget = self.review_controller().widget
            if mode == "input":
                self.component_manager.register(w_class)
                widget = self.component_manager.get_current("add_cards_dialog")
            else:
                widget = w_class(self.component_manager)
            self.widgets[mode] = widget

        widget.activate(param)

    def start(self, mode):
        """UI entry point. Activates specified mode."""

        if not mode:
            if self.config()['startup_with_review']:
                mode = 'review'
            else:
                mode = 'menu'

        getattr(self, mode + '_')()
        gtk.main()

    def custom_handler(self, glade, function_name, widget_name, *args):
        """Hook for custom widgets."""

        if glade and widget_name and  hasattr(self, function_name):
            handler = getattr(self, function_name)
            return handler(args)

    def start_playing(self, text, parent):
        """Start playing audiofile."""

        if not self.soundmanager:
            from pomni.sound import SoundPlayer
            self.soundmanager = SoundPlayer()
        self.soundmanager.play(self.soundmanager.parse_fname(text), parent)

    def stop_playing(self):
        """Stop playing audiofile."""

        if self.soundmanager:
            self.soundmanager.stop()

    # modes
    def menu_(self):
        """Activate menu."""
        self.activate_mode('menu', None)

    def input_(self, widget=None):
        """Activate input mode through main ui controller."""
        self.controller().add_cards()

    def configure_(self, widget=None):
        """Activate configure mode through main ui controller."""
        self.controller().configure()

    def review_(self, widget=None):
        """Activate review mode."""
        self.activate_mode('review', None)

    def exit_(self, widget):
        """Exit from main gtk loop."""
        gtk.main_quit()

    # gtk window callbacks
    def window_keypress_cb(self, widget, event, *args):
        """Key pressed."""

        if event.keyval == gtk.keysyms.F6:
            # The "Full screen" hardware key has been pressed
            if self.fullscreen:
                self.window.unfullscreen()
            else:
                self.window.fullscreen()
            self.fullscreen = not self.fullscreen


    def window_state_cb(self, widget, event):
        """Checking window state."""

        self.fullscreen = bool(event.new_window_state & \
            gtk.gdk.WINDOW_STATE_FULLSCREEN)


    # ui helpers
    @staticmethod
    def create_gtkhtml(args):
        """ Create gtkhtml2 widget """

        def request_url(document, url, stream):
            uri = urlparse.urljoin("", url)
            f = htmlOpener.open(uri)
            stream.write(f.read())
            stream.close()

        view = gtkhtml2.View()
        document = gtkhtml2.Document()
        document.connect('request_url', request_url)
        view.set_document(document)
        view.document = document
        view.show()
        return view

    # Main Widget API
    def information_box(self, message):
        """Show Information message."""

        self.information_dialog_label.set_text('\n' + message + '\n')
        self.information_dialog.run()
        self.information_dialog.hide()

    def question_box(self, question, option0, option1, option2):
        """Show Question message."""

        self.question_dialog_label.set_text( \
            '\n'  + question.replace("?", "?\n").replace(",", ",\n"))
        response = self.question_dialog.run()
        self.question_dialog.hide()
        if response == gtk.RESPONSE_YES:
            return False
        return True

    def run_edit_fact_dialog(self, fact, allow_cancel=True):
        """Activate input mode."""

        self.activate_mode('input', fact) 

    def run_add_cards_dialog(self):
        """Activate input mode."""

        self.activate_mode('input', None)

    def run_configuration_dialog(self):
        """Activate configuration mode."""

        self.activate_mode('configuration', None)



# Local Variables:
# mode: python
# py-indent-offset: 4
# indent-tabs-mode nil
# tab-width 4
# End:
