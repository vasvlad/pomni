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
        self.theme = self.config()["theme_path"].split("/")[-1]
        theme_path = self.config()["theme_path"]
        gtk.rc_parse(os.path.join(theme_path, "rcfile"))
        gtk.glade.set_custom_handler(self.custom_handler)
        w_tree = gtk.glade.XML(os.path.join(theme_path, "window.glade"))

        # Set unvisible tabs of switcher
        self.switcher = w_tree.get_widget("switcher")
        self.switcher.set_property('show_tabs', False)
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
            widget = getattr(module, cname)(self.component_manager)
            self.widgets[mode] = widget
            if mode == "review":
                self.component_manager.register(widget)

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
        self.ui_controller_main().add_cards()

    def configure_(self, widget=None):
        """Activate configure mode through main ui controller."""
        self.ui_controller_main().configure()

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


    @staticmethod
    def clear_label(caption):
        """Remove &-symbol from caption if exists."""
        index = caption.find("&")
        if not index == -1:
            return caption[:index] + caption[index+1:]
        return caption


    # Main Widget API
    def information_box(self, message, button_caption='OK'):
        """Create Information message."""
        dialog = self.w_tree.get_widget("information_dialog")
        self.w_tree.get_widget("information_dialog_label").set_text(\
            '\n' + "  " + message + "  " + '\n')
        self.w_tree.get_widget("information_dialog_button_ok").set_label(\
            button_caption)
        dialog.run()
        dialog.hide()


    def question_box(self, question, option0, option1, option2):
        """Create Question message."""
        dialog = self.w_tree.get_widget("question_dialog")
        dialog_label = self.w_tree.get_widget("question_dialog_label")
        question = question.replace("?", "?\n")
        question = question.replace(",", ",\n")
        dialog_label.set_text('\n'  + question)
        result = True
        response = dialog.run()
        if response == -8:
            result = False
        dialog.hide()
        return result


    def update_status_bar(self, message=None):
        """ Not Implemented """
        print 'update_status_bar'


    def run_edit_fact_dialog(self, fact, allow_cancel=True):
        """Start Edit/Update window."""

        self.activate_mode('input', fact) 

    def error_box(self, message):
        print 'error_box', message
    
    def save_file_dialog(self, path, filter, caption=""):
        print 'save_file_dialog'
    
    def open_file_dialog(self, path, filter, caption=""):
        print 'open_file_dialog'

    def set_window_title(self, title):
        #print 'set_window_title'
        pass

    def run_add_cards_dialog(self):
        self.activate_mode('input', None)

    def run_edit_deck_dialog(self):
        print 'edit_deck_dialog'
    
    def run_configuration_dialog(self):
        self.activate_mode('configuration', None)

    def run_card_appearance_dialog(self):
        print 'run_card_appearance_dialog'

    def run_manage_card_types_dialog(self):
        print 'run_manage_card_types_dialog'


# Local Variables:
# mode: python
# py-indent-offset: 4
# indent-tabs-mode nil
# tab-width 4
# End:
