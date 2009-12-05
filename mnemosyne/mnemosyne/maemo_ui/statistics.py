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
Hildon UI. Statistics Widget.
"""

import os
import time
from mnemosyne.maemo_ui.widgets import create_statistics_ui
from mnemosyne.libmnemosyne.ui_component import UiComponent

DAY = 24 * 60 * 60 # Seconds in a day.

class MaemoStatisticsWidget(UiComponent):
    """Statistics Widget."""


    def __init__(self, component_manager):
        UiComponent.__init__(self, component_manager, )
        self.html = ""
        # create widgets
        self.page, menu_button = create_statistics_ui(self.main_widget().switcher, \
            os.path.join(self.config()['theme_path'], "mnemosyne.png"))
        # connect signals
        menu_button.connect('clicked', self.statistics_to_main_menu_cb)

    def prepare_statistics(self):
        card = self.review_controller().card
        self.html = """<html<body>
        <style type="text/css">
        table { height: 100%;
                margin-left: auto; margin-right: auto;
                text-align: center}
        body  { background-color: white;
                margin: 0;
                padding: 0;
                border: thin solid #8F8F8F; }
        </style></head><table><tr><td>"""
        if not card:
            self.html += "No current card."
        elif card.grade == -1:
            self.html += "Unseen card, no statistics available yet."
        else:
            self.html += "Grade" + ": %d<br>" % card.grade
            self.html += "Easiness" + ": %1.2f<br>" % card.easiness
            self.html += "Repetitions" + ": %d<br>" \
                % (card.acq_reps + card.ret_reps)
            self.html += "Lapses" + ": %d<br>" % card.lapses
            self.html += "Interval" + ": %d<br>" \
                % (card.interval / DAY)
            self.html += "Last repetition" + ": %s<br>" \
                % time.strftime("%B %d, %Y", time.gmtime(card.last_rep))           
            self.html += "Next repetition" + ": %s<br>" \
                % time.strftime("%B %d, %Y", time.gmtime(card.next_rep))
            self.html += "Average thinking time (secs)" + ": %d<br>" \
                % self.database().average_thinking_time(card)
            self.html += "Total thinking time (secs)" + ": %d<br>" \
                % self.database().total_thinking_time(card)
        self.html += "</td></tr></table></body></html>"

    def activate(self):
        """Set necessary switcher page."""
        print "activate"
        self.prepare_statistics()
        print self.html
        self.main_widget().switcher.set_current_page(self.page)
        
    def statistics_to_main_menu_cb(self, widget):
        """Returns to main menu."""

        self.main_widget().switcher.remove_page(self.page)
        self.main_widget().menu_('statistics')
       
