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

from mnemosyne.libmnemosyne.ui_component import UiComponent
from mnemosyne.libmnemosyne.ui_components.main_widget import MainWidget

_ = gettext.gettext


class HildonUiException(Exception):
    """ Exception hook """

    def __init__(self, w_tree, exception):
        """Show Warning Window."""

        dialog = w_tree.get_widget("information_dialog")
        w_tree.get_widget("information_dialog_label").set_text(\
            '\n' + "  " + exception + "  " + '\n')
        dialog.run()
        dialog.hide()

        Exception.__init__(self)


class HildonMainWidget(MainWidget):
    """Hildon main widget."""

    menu, review, input, configuration = range(4)

    def activate(self):
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

        self.spliter_trigger = True
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
            for sig in ("window_state", "window_keypress", "size_allocate")]))

        self.w_tree = w_tree
        print 'HildonUI.activate finished', self

    def activate_mode(self, mode):
        """Activate mode in lazy way."""

        self.switcher.set_current_page(getattr(self, mode))
        widget = self.widgets.get(mode, None)
        if not widget: # lazy widget creation
            cname = self.theme.capitalize() + '%sWidget' % mode.capitalize()
            module = __import__("pomni.%s" % mode, globals(),
                                locals(), [cname])
            widget = getattr(module, cname)(self.component_manager)
            self.widgets[mode] = widget

        widget.activate()

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

    # modes
    def menu_(self):
        """Activate menu."""
        self.activate_mode('menu')

    def input_(self, widget=None):
        """Activate input mode through main ui controller."""
        self.ui_controller_main().add_cards()

    def configure_(self, widget=None):
        """Activate configure mode through main ui controller."""
        self.ui_controller_main().configure()

    def review_(self, widget=None):
        """Activate review mode."""
        self.review_widget().activate()

    def exit_(self, widget):
        """Exit from main gtk loop."""
        gtk.main_quit()

    # gtk window callbacks
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

        view = gtkhtml2.View()
        document = gtkhtml2.Document()
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
        dialog_label.set_text('\n' + "  " + question + "  " + '\n')
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
        print 'run_edit_fact_dialog'


    def error_box(self, message):
        print 'error_box', message
    
    def save_file_dialog(self, path, filter, caption=""):
        print 'save_file_dialog'
    
    def open_file_dialog(self, path, filter, caption=""):
        print 'open_file_dialog'

    def set_window_title(self, title):
        print 'set_window_title'

    def run_add_cards_dialog(self):
        self.activate_mode('input')

    def run_edit_deck_dialog(self):
        print 'edit_deck_dialog'
    
    def run_configuration_dialog(self):
        self.activate_mode('configuration')

    def run_edit_fact_dialog(self, fact, allow_cancel=True):
        print 'run_edit_fact_dialog'
    
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
