#!/usr/bin/python -tt
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
Programming of "eternal" design 
"""

from pomni.hildon_ui import HildonUiControllerReview

class HildonThemeUiControllerReview(HildonUiControllerReview):
    """ Child of HildonUiControllerReview especialy for Etrenal theme """

    def __init__(self):
        """ Initialization items of review window for Eternal theme """

        HildonUiControllerReview.__init__(self)
        self.get_answer_hbox = None
        self.estimate_box = None
        self.answer_box = None
        self.answer_box = None
        self.w_tree = None

    def show_answer(self):
        """ Show answer in review window for eternal theme """

        self.get_answer_hbox.set_property('visible', False)
        self.estimate_box.set_property('visible', True)
        self.answer_box.set_property('visible', True)
        self.answer.set_text(self.card.answer())

    def start(self, w_tree):
        """ Start new review window for eternal theme """

        HildonUiControllerReview.start(self, w_tree)
        self.get_answer_hbox = self.w_tree.get_widget("get_answer_hbox")
        self.estimate_box = self.w_tree.get_widget("estimate_box")
        self.answer_box = self.w_tree.get_widget("answer_box")

        #Connect to various signals
        self.w_tree.signal_autoconnect({
           "on_eventbox_show_answer_button_press_event": self.open_card_clicked
        })

        #Begin the review window from a new question
        self.new_question()


    def theme_new_question(self):
        """ Visible and Unvisible some items of review windows """
        self.estimate_box.set_property('visible', False)
        self.answer_box.set_property('visible', False)
        self.get_answer_hbox.set_property('visible', True)


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
