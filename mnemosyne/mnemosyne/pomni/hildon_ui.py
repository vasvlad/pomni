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

from mnemosyne.libmnemosyne.ui_component import UiComponent
from mnemosyne.libmnemosyne.ui_components.main_widget import MainWidget

_ = gettext.gettext


class HildonUiControllerException(Exception):
    """ Exception hook """

    def __init__(self, w_tree, exception):
        """Show Warning Window."""

        dialog = w_tree.get_widget("information_dialog")
        w_tree.get_widget("information_dialog_label").set_text(\
            '\n' + "  " + exception + "  " + '\n')
        dialog.run()
        dialog.hide()

        Exception.__init__(self)


class HildonBaseController(UiComponent):
    """Base controllers functionality."""

    main_menu, review, input, configuration = range(4)

    def __init__(self, component_manager):
        """Attributes initialization."""

        print 'HildonBaseController.__init__'
        UiComponent.__init__(self, component_manager)

    def __getattr__(self, name):
        """Lazy get widget as an attribute."""

        if 'w_tree' not in self.__dict__:
            self.w_tree = self.main_widget().w_tree

        widget = self.w_tree.get_widget(name)
        if widget:
            return widget
        raise AttributeError()

    def to_main_menu_cb(self, widget):
        """Returns to main menu."""

        self.switcher.set_current_page(self.main_menu)

class HildonMainWidget(MainWidget):
    """Hildon main widget."""

    main_menu, review, input, configuration = range(4)

    #def __init__(self, component_manager):
    #    MainWidget.__init__(self, component_manager)
    #    #self.w_tree = None

    def activate(self):
        print 'HildonMainWidget.activate'
        def gen_callback(mode):
            """Generate callback for mode."""

            def callback(widget, event = None):
                """Callback function."""
                self.controllers[mode].show()
            return callback

        try:
            theme = self.config()["theme_path"].split("/")[-1]
        except KeyError:
            locals()["theme"] = "eternal"

        # Load the glade file for current theme
        #ui_controller_main().widget = self
        theme_path = self.config()["theme_path"]
        gtk.rc_parse(os.path.join(theme_path, "rcfile"))
        gtk.glade.set_custom_handler(self.custom_handler)
        w_tree = gtk.glade.XML(os.path.join(theme_path, "window.glade"))

        #controllers = {}
        #for mode in ("input", "configure") #, "main", "review"):
        #    cname = theme.capitalize() + 'Controller' + mode.capitalize()
        #    module = __import__("pomni.hildon_%s" % mode, 
        #            globals(), locals(), [cname])
        #    print cname
        #    controllers[mode] = getattr(module, cname)(self.component_manager)
        #    #controllers[mode].activate()

        # Set unvisible tabs of switcher
        self.switcher = w_tree.get_widget("switcher")
        self.switcher.set_property('show_tabs', False)
        self.window = w_tree.get_widget("window")
        self.window.connect('delete_event', self.exit_cb)

        self.spliter_trigger = True
        self.question_flag = False
        # fullscreen mode
        if self.config()['fullscreen']:
            self.window.fullscreen()
            self.fullscreen = True
        else:
            self.fullscreen = False

        # Generate callbacks for modes
        #self.controllers = controllers
        #print 'assigned controllers to', self
        #signals = ["review", "input", "configure"]
        #for signal in signals:
        #    setattr(self, signal + '_cb', gen_callback(signal))

        #self.signals = ["exit", "window_state", "window_keypress"] + signals

        # connect signals to methods
        w_tree.signal_autoconnect(dict([(sig, getattr(self, sig + "_cb")) \
            for sig in ("exit", "window_state", "window_keypress", "size_allocate")]))

        self.w_tree = w_tree

        print 'HildonUI.activate finished', self


    def show(self): #, mode):
        """Start UI."""

        #self.controllers[mode].show()
        self.switcher.set_current_page(self.main_menu)
        gtk.main()

    def custom_handler(self, glade, function_name, widget_name, *args):
        """Hook for custom widgets."""

        if glade and widget_name and  hasattr(self, function_name):
            handler = getattr(self, function_name)
            return handler(args)

    # Callbacks
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

    def exit_cb(self, widget=None):
        """If pressed quit button then close the window."""

        self.database().unload()
        gtk.main_quit()


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
    
    def information_box(self, message, button_caption):
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
        pass


    def run_edit_fact_dialog(self, fact, allow_cancel=True):
        """Start Edit/Update window."""

        self.controllers['input'].activate(fact)

    def information_box(self, message):
        pass
            
    def question_box(self, question, option0, option1, option2):
        pass
    
    def error_box(self, message):
        pass
    
    def save_file_dialog(self, path, filter, caption=""):
        pass
    
    def open_file_dialog(self, path, filter, caption=""):
        pass

    def set_window_title(self, title):
        pass
    
    def run_add_card_dialog(self):
        pass

    def run_edit_fact_dialog(self, fact, allow_cancel=True):
        pass
    
    def run_card_appearance_dialog(self):
        pass

    def run_manage_card_types_dialog(self):
        pass



# Local Variables:
# mode: python
# py-indent-offset: 4
# indent-tabs-mode nil
# tab-width 4
# End:
