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
Programming of "draft" design 
"""
import os
import gettext
from os.path import basename

def theme_start(self):

    self.eventbox_show_answer = self.w_tree.get_widget("eventbox_show_answer")
    #Connect to various signals
    self.w_tree.signal_autoconnect({"on_eventbox_numeral0_button_press_event": self.numeral0_pressed,
                                  "on_eventbox_numeral1_button_press_event": self.numeral1_pressed,
                                  "on_eventbox_numeral2_button_press_event": self.numeral2_pressed,
                                  "on_eventbox_numeral3_button_press_event": self.numeral3_pressed,
                                  "on_eventbox_numeral4_button_press_event": self.numeral4_pressed,
                                  "on_eventbox_numeral5_button_press_event": self.numeral5_pressed,
                                  "on_eventbox_show_answer_button_press_event": self.open_card_clicked,
                                  "on_exit_clicked" : self.quit})


def theme_show_answer(self):

    self.answer.set_text(self.card.answer())
    self.eventbox_numeral0.set_sensitive(True)
    self.eventbox_numeral1.set_sensitive(True)
    self.eventbox_numeral2.set_sensitive(True)
    self.eventbox_numeral3.set_sensitive(True)
    self.eventbox_numeral4.set_sensitive(True)
    self.eventbox_numeral5.set_sensitive(True)
    self.eventbox_show_answer.set_sensitive(False)

def theme_new_question(self):

    self.eventbox_numeral0.set_sensitive(False)
    self.eventbox_numeral1.set_sensitive(False)
    self.eventbox_numeral2.set_sensitive(False)
    self.eventbox_numeral3.set_sensitive(False)
    self.eventbox_numeral4.set_sensitive(False)
    self.eventbox_numeral5.set_sensitive(False)
    self.eventbox_show_answer.set_sensitive(True)

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
