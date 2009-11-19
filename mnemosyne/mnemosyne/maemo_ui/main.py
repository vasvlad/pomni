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
import gtk
import urllib
import gtkhtml2
import urlparse

from mnemosyne.maemo_ui.sound import SoundPlayer
from mnemosyne.libmnemosyne.ui_components.main_widget import MainWidget


class MainWdgt(MainWidget):
    """Main widget class."""

    menu, review, input, configuration, sync, about, tags = range(7)

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
        """Basic UI setup."""

        # Load the glade file for current theme
        theme_path = self.config()["theme_path"]
        self.theme = theme_path.split("/")[-1]
        gtk.rc_parse(os.path.join(theme_path, "rcfile"))

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.resize(800, 480)
        self.window.set_name('window')
        self.switcher = gtk.Notebook()
        self.switcher.set_show_border(False)
        self.switcher.set_show_tabs(False)
        self.window.add(self.switcher)

        # fullscreen mode
        self.fullscreen = self.config()['fullscreen']
        if self.fullscreen:
            self.window.fullscreen()
        # connect signals to methods
        self.window.connect("delete_event", self.exit_)
        self.window.connect('window-state-event', self.window_state_cb)
        self.window.connect('key-press-event', self.window_keypress_cb)

        self.window.show_all()

    def activate_mode(self, mode):
        """Activate mode in lazy way."""

        widget = self.create_mode(mode)
        widget.activate()

    def create_mode(self, mode):
        """Create widget object for selected mode."""

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
            elif mode == "tags":
                from mnemosyne.maemo_ui.tags import TagsWidget
                widget = TagsWidget(self.component_manager)
            self.widgets[mode] = widget
        return widget

    def start(self, mode):
        """UI entry point. Activates specified mode."""

        if not mode:
            if self.config()['startup_with_review']:
                self.review_()
            else:
                self.menu_()
        gtk.main()

    def kill_menu_object(self):
        """Removes MenuWidget object from memory."""

        if 'menu' in self.widgets:
            del self.widgets['menu']

    # modes
    def menu_(self, mode=None):
        """Activate menu."""

        if mode is not None:
            del self.widgets[mode]
        self.activate_mode('menu')

    def tags_(self):
        """Activate 'Activate tags' mode."""

        self.kill_menu_object()
        if 'review' not in self.widgets:
            self.create_mode('review')
        self.controller().activate_cards()

    def input_(self):
        """Activate input mode."""
       
        if 'review' not in self.widgets:
            self.create_mode('review')
        self.show_mode("input")
        self.controller().add_cards()

    def configure_(self):
        """Activate configure mode through main controller."""

        if 'review' not in self.widgets:
            self.create_mode('review')
        self.show_mode('configuration')
        self.controller().configure()

    def review_(self):
        """Activate review mode."""

        self.kill_menu_object()
        self.activate_mode('review')

    def sync_(self):
        """Activate sync mode."""

        self.activate_mode('sync')

    def about_(self):
        """Activate about mode."""

        self.kill_menu_object()
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
    def create_gtkhtml(self):
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

        dialog = gtk.Dialog(parent=self.window, flags=gtk.DIALOG_MODAL|\
            gtk.DIALOG_DESTROY_WITH_PARENT|gtk.DIALOG_NO_SEPARATOR)
        dialog.set_decorated(False)
        button_ok = dialog.add_button('OK', gtk.RESPONSE_OK)
        button_ok.set_size_request(120, 80)
        button_ok.set_name('dialog_button')
        label = gtk.Label()
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.set_name('information_dialog_label')
        label.set_text('\n   ' + message.replace('.', '.   \n').replace( \
            ',', ',\n') + '\n')
        label.show()
        dialog.vbox.pack_start(label)
        dialog.action_area.set_layout(gtk.BUTTONBOX_SPREAD)
        dialog.run()
        dialog.destroy()

    def error_box(self, message):
        """Error message."""

        self.information_box(message)

    def question_box(self, question, option0, option1, option2):
        """Show Question message."""

        dialog = gtk.Dialog(parent=self.window, flags=gtk.DIALOG_MODAL|\
            gtk.DIALOG_DESTROY_WITH_PARENT|gtk.DIALOG_NO_SEPARATOR)
        dialog.set_decorated(False)
        button_yes = dialog.add_button('YES', gtk.RESPONSE_YES)
        button_yes.set_size_request(120, 80)
        button_yes.set_name('dialog_button')
        button_no = dialog.add_button('NO', gtk.RESPONSE_REJECT)
        button_no.set_size_request(120, 80)
        button_no.set_name('dialog_button')
        label = gtk.Label()
        label.set_name('question_dialog_label')
        label.set_text('\n' + question.replace('?', '?\n').replace(',', ',\n') \
            + '\n')
        label.show()
        dialog.vbox.pack_start(label)
        dialog.vbox.set_spacing(2)
        response = dialog.run()
        dialog.destroy()
        if response == gtk.RESPONSE_YES:
            return False
        return True


# Local Variables:
# mode: python
# py-indent-offset: 4
# indent-tabs-mode nil
# tab-width 4
# End:
