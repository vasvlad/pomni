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
import os
import gettext
from os.path import basename

"""
Programming of "eternal" design 
"""
def theme_start(self):

    self.get_answer_hbox = self.w_tree.get_widget("get_answer_hbox")
    self.estimate_box = self.w_tree.get_widget("estimate_box")
    self.answer_box = self.w_tree.get_widget("answer_box")

    #Connect to various signals
    self.w_tree.signal_autoconnect({"on_eventbox_numeral0_button_press_event": self.numeral_pressed,
                                  "on_eventbox_numeral1_button_press_event": self.numeral_pressed,
                                  "on_eventbox_numeral2_button_press_event": self.numeral_pressed,
                                  "on_eventbox_numeral3_button_press_event": self.numeral_pressed,
                                  "on_eventbox_numeral4_button_press_event": self.numeral_pressed,
                                  "on_eventbox_numeral5_button_press_event": self.numeral_pressed,
                                  "on_eventbox_show_answer_button_press_event": self.open_card_clicked,
                                  "on_eventbox_quit_button_press_event": self.quit_button,
                                  "on_exit_clicked" : self.quit})


def theme_show_answer(self):

    self.get_answer_hbox.set_property('visible', False)
    self.estimate_box.set_property('visible', True)
    self.answer_box.set_property('visible', True)
    self.answer.set_text(self.card.answer())

def theme_new_question(self):

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
