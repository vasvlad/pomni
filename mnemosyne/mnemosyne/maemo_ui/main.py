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

import mnemosyne.maemo_ui.widgets.main as widgets

from mnemosyne.libmnemosyne.ui_components.main_widget import MainWidget

class MainWdgt(MainWidget):
    """Main widget class."""

    def __init__(self, component_manager):
        MainWidget.__init__(self, component_manager)
        self.window = None
        self.switcher = None
        self.widgets = {}
        self._soundplayer = None

    @property
    def soundplayer(self):
        if not self._soundplayer:
            from mnemosyne.maemo_ui.sound import SoundPlayer
            self._soundplayer = SoundPlayer()
        return self._soundplayer

    def activate(self):
        """Basic UI setup."""

        # load styles
        gtk.rc_parse(os.path.join(self.config()["theme_path"], "rcfile"))
        # create main window
        self.window, self.switcher = widgets.create_main_ui()
        # fullscreen mode
        fullscreen = self.config()['fullscreen']
        if fullscreen:
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
            elif mode == "statistics":
                from mnemosyne.maemo_ui.statistics import MaemoStatisticsWidget
                widget = MaemoStatisticsWidget(self.component_manager, "Menu")
            elif mode == "importcards":
                from mnemosyne.maemo_ui.importcards import ImportCardsWidget 
                self.review_controller().reset()
                widget = ImportCardsWidget(self.component_manager)

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

    def input_(self, mode=None):
        """Activate input mode."""
       
        self.kill_menu_object()
        if 'review' not in self.widgets:
            self.create_mode('review')
        #self.controller().add_cards()
        self.component_manager.get_current("add_cards_dialog")\
            (self.component_manager).activate(mode)

    def configure_(self):
        """Activate configure mode through main controller."""

        self.kill_menu_object()
        if 'review' not in self.widgets:
            self.create_mode('review')
        self.controller().configure()

    def review_(self):
        """Activate review mode."""

        self.kill_menu_object()
        self.activate_mode('review')

    def statistics_(self):
        """Activate statistics mode."""

        self.kill_menu_object()
        self.activate_mode('statistics')

    def import_(self):
        """Activate import mode."""

        self.kill_menu_object()
        self.activate_mode('importcards')

    def sync_(self):
        """Activate sync mode."""

        self.kill_menu_object()
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

    # Main Widget API
    def information_box(self, message):
        """Show Information message."""

        widgets.create_information_dialog(self.window, message)

    def error_box(self, message):
        """Error message."""

        self.information_box(message)

    def question_box(self, question, option0, option1, option2):
        """Show Question message."""

        return widgets.create_question_dialog(self.window, question) 
        


# Local Variables:
# mode: python
# py-indent-offset: 4
# indent-tabs-mode nil
# tab-width 4
# End:
