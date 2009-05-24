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
Hildon UI. Main mode controllers.
"""

from pomni.hildon_ui import HildonBaseUi


class HildonUiControllerMain(HildonBaseUi):
    """ Hidon Main Controller  """

    def __init__(self, w_tree, signals=None):

        HildonBaseUi.__init__(self, w_tree, signals)

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

    def __init__(self, w_tree):
        """ Added spliter widget to class """

        self.base = HildonUiControllerMain
        self.base.__init__(self, w_tree, ["size_allocate"])
        self.spliter_trigger = True

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

    def start(self):
        """ Start base class """
        HildonBaseUi.start(self, self.main_menu)

class RainbowControllerMain(HildonUiControllerMain):
    """ Rainbow UI Main Controller """

    def __init__(self, w_tree):
        """ Added spliter widget to class """

        self.base = HildonUiControllerMain
        self.base.__init__(self, w_tree, [])
        self.spliter_trigger = True

    def start(self, ):
        """ Start base class """

        self.switcher.set_current_page(self.main_menu)


# Local Variables:
# mode: python
# py-indent-offset: 4
# indent-tabs-mode nil
# tab-width 4
# End:
