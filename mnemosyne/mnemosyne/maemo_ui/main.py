#!/usr/bin/python -tt
# vim: sw=4 ts=4 expandtab ai
#
# Mnemosyne. Learning tool based on spaced repetition technique
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
Main Widget.
"""

import os
import gettext
import gtk
import gtk.glade
import urllib
import gtkhtml2
import urlparse
import gobject

from mnemosyne.maemo_ui.sound import SoundPlayer
from mnemosyne.libmnemosyne.ui_components.main_widget import MainWidget

_ = gettext.gettext

class MainWdgt(MainWidget):
    """Main widget class."""

    menu, review, input, configuration, sync, about = range(6)

    def __init__(self, component_manager):
        MainWidget.__init__(self, component_manager)
        self.switcher = self.question_dialog = self.window = self.w_tree = \
            self.question_dialog_label = self.information_dialog = \
            self.information_dialog_label  = self.theme = \
            self.fullscreen = None
        self.htmlopener = urllib.FancyURLopener()
        self.widgets = {}
        self.soundplayer = SoundPlayer()

    def activate(self):
        """Basic UI setup. 
           Load theme glade file, assign gtk window callbacks.
        """

        # Load the glade file for current theme
        theme_path = self.config()["theme_path"]
        self.theme = theme_path.split("/")[-1]
        gtk.rc_parse(os.path.join(theme_path, "rcfile"))
        gtk.glade.set_custom_handler(self.custom_handler)
        w_tree = gtk.glade.XML(os.path.join(theme_path, "window.glade"))
        get_widget = w_tree.get_widget

        self.switcher = get_widget("switcher")
        self.window = get_widget("window")

        # fullscreen mode
        self.fullscreen = self.config()['fullscreen']
        if self.fullscreen:
            self.window.fullscreen()

        # connect signals to methods
        self.window.connect("delete_event", self.exit_)
        w_tree.signal_autoconnect(dict([(sig, getattr(self, sig + "_cb")) \
            for sig in ("window_state", "window_keypress")]))

        self.question_dialog = get_widget("question_dialog")
        self.information_dialog = get_widget("information_dialog")
        self.question_dialog_label = get_widget("question_dialog_label")
        self.information_dialog_label = get_widget("information_dialog_label")

        self.w_tree = w_tree

    def show_mode(self, mode):
        self.switcher.set_current_page(getattr(self, mode))

    def activate_mode(self, mode):
        """Activate review or menu mode in lazy way."""

        self.show_mode(mode)
        widget = self.widgets.get(mode, None)
        if not widget: # lazy widget creation
            if mode == "review":
                self.review_controller().reset()
                widget = self.review_controller().widget
            elif mode == "menu":
                from mnemosyne.maemo_ui.menu import MenuWidget
                widget = MenuWidget(self.component_manager)
            elif mode == "sync":
                from mnemosyne.maemo_ui.sync import SyncWidget
                widget = SyncWidget(self.component_manager)
            elif mode == "about":
                from mnemosyne.maemo_ui.about import AboutWidget
                widget = AboutWidget(self.component_manager)
            self.widgets[mode] = widget

        widget.activate()

    def start(self, mode):
        """UI entry point. Activates specified mode."""

        if not mode:
            if self.config()['startup_with_review']:
                self.review_()
            else:
                self.menu_()
        gtk.main()

    def custom_handler(self, glade, function_name, widget_name, *args):
        """Hook for custom widgets."""

        if glade and widget_name and  hasattr(self, function_name):
            handler = getattr(self, function_name)
            return handler(args)

    # modes
    def menu_(self):
        """Activate menu."""
        self.activate_mode('menu')

    def input_(self):
        """Activate input mode."""
       
        # reset review controller if needed
        if "review" not in self.widgets:
            self.show_mode("review") # without this line 
                                     # "window" widget is not defined 
            self.review_controller().reset()
            self.widgets["review"] = self.review_controller().widget

        self.show_mode("input")
        self.controller().add_cards()

    def configure_(self):
        """Activate configure mode through main controller."""
        self.show_mode("configuration")
        self.controller().configure()

    def review_(self):
        """Activate review mode."""
        self.activate_mode('review')

    def sync_(self):
        """Activate sync mode."""
        self.activate_mode('sync')

    def about_(self):
        """Activate about mode."""
        self.activate_mode('about')

    @staticmethod
    def exit_(window=None, event=None):
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
    def create_gtkhtml(self, args):
        """ Create gtkhtml2 widget """

        def request_url(document, url, stream):
            """Get content from url."""
            uri = urlparse.urljoin("", url)
            fpurl = self.htmlopener.open(uri)
            stream.write(fpurl.read())
            fpurl.close()
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

    def error_box(self, message):
        """Error message."""

        self.information_box(message)

    def question_box(self, question, option0, option1, option2):
        """Show Question message."""

        self.question_dialog_label.set_text( \
            '\n'  + question.replace("?", "?\n").replace(",", ",\n"))
        response = self.question_dialog.run()
        self.question_dialog.hide()
        if response == gtk.RESPONSE_YES:
            return False
        return True


# Local Variables:
# mode: python
# py-indent-offset: 4
# indent-tabs-mode nil
# tab-width 4
# End:
