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

from mnemosyne.libmnemosyne.component_manager import config
from pomni.hildon_ui import HildonBaseUi


class HildonUiControllerConfigure(HildonBaseUi):
    """ Hildon Config controller """

    def __init__(self):
        """ Initialization items of config window """
        HildonBaseUi.__init__(self,  signals = ['change_fullscreen', \
                    'change_font_size','change_startup_with_review'])
        self.modified = False
        self.configuration = config()

    def start(self, w_tree):
        """ Start config window """
        self.w_tree = w_tree
        HildonBaseUi.start(self, w_tree)
        self.checkbox_fullscreen_mode.set_active(
            self.configuration['fullscreen'])
        self.checkbox_start_in_review_mode.set_active(
            self.configuration['startup_with_review'])
        self.spinbutton_fontsize.set_value(self.configuration['font_size'])
        self.switcher.set_current_page(self.config)

    def change_fullscreen_cb(self, widget):
        """ Change Fullscreen parameter """
        self.modified = True
        self.configuration['fullscreen'] = \
            self.checkbox_fullscreen_mode.get_active()

    def change_font_size_cb(self, widget):
        """ Change Font size parameter """
        self.modified = True
        self.configuration['font_size'] = \
            self.spinbutton_fontsize.get_value_as_int()

    def change_startup_with_review_cb(self, widget):
        """ Change 'Startup with Review' parameter """
        self.modified = True
        self.configuration['startup_with_review'] = \
            self.checkbox_start_in_review_mode.get_active()

    def to_main_menu_cb(self, widget, event):
        """ Return to main menu """
        if self.modified:
            self.configuration.save()
        self.switcher.set_current_page(self.main_menu)

class EternalControllerConfigure(HildonUiControllerConfigure):
    """Eternal Configure controller. Nothing special."""
    pass


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
