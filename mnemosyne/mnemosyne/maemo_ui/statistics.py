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
Hildon UI. Statistics widget.
"""

import time
from mnemosyne.libmnemosyne.ui_components.dialogs import StatisticsDialog
from mnemosyne.maemo_ui.widgets.statistics import create_statistics_ui

DAY = 24 * 60 * 60 # Seconds in a day.

class MaemoStatisticsWidget(StatisticsDialog):
    """Statistics Widget."""

    def __init__(self, component_manager, previous_mode=None):
        StatisticsDialog.__init__(self, component_manager)
        self.renderer = self.component_manager.get_current('renderer')
        self.html = '<html><head><meta http-equiv="Content-Type" content='\
        '"text/html;charset=UTF-8"><style type="text/css">*{font-size:28px;'\
        'font-family:Nokia Sans} table {height:100%;margin-left:auto;margin-'\
        'right:auto;text-align:center} body{ background-color:white;margin:0;'\
        'padding:0;}</style></head><body><table>'
        self.tags_text = {}
        # create widgets
        self.page, self.mode_statistics_switcher, menu_button, \
            current_card_button, common_button, tags_button, \
            self.current_card_html_widget, self.total_card_html_widget, \
            self.tags_html_widget = create_statistics_ui( \
                self.main_widget().switcher)
        # connect signals
        if previous_mode == 'Menu':
            menu_button.connect('clicked', self.back_to_main_menu_cb)
        else:
            menu_button.connect('clicked', self.back_to_previous_mode_cb)

        current_card_button.connect('released', self.current_card_statistics_cb)
        common_button.connect('released', self.common_statistics_cb)
        tags_button.connect('released', self.tags_statistics_cb)

        #Change current page
        if "last_variant_for_statistics_page" in self.config():
            number_of_page = self.config()["last_variant_for_statistics_page"] 
        else:
            number_of_page = 2
        if number_of_page == 0:
            current_card_button.set_active(True)
            self.current_card_statistics_cb(None)
        elif number_of_page == 2:
            tags_button.set_active(True)
            self.tags_statistics_cb(None) 
        else:
            common_button.set_active(True)
            self.common_statistics_cb(None) 
 
    def activate(self):
        """Set necessary switcher page."""

        self.main_widget().switcher.set_current_page(self.page)

    def back_to_previous_mode_cb(self, widget):
        """Returns to previous menu."""

        self.config()["last_variant_for_statistics_page"] = \
            self.mode_statistics_switcher.get_current_page()
        self.main_widget().switcher.remove_page(self.page)

    def back_to_main_menu_cb(self, widget):
        """Returns to main menu."""

        self.config()["last_variant_for_statistics_page"] = \
            self.mode_statistics_switcher.get_current_page()
        self.main_widget().switcher.remove_page(self.page)
        self.main_widget().menu_('statistics')

    # callbacks
    def current_card_statistics_cb(self, widget):
        """Switches to the current card statistics page."""

        card = self.review_controller().card
        html = self.html
        if not card:
            html += "<tr><td><b>No current card</b></td></tr>"
        elif card.grade == -1:
            html += "<tr><td><b>Unseen card, no statistics available " \
                "yet</b></td></tr>"
        else:
            html += "<tr><td><b>Current card statistics<br><br></b></td></tr>"
            html += "<tr><td>Grade" + ": %d</td></tr>" % card.grade
            html += "<tr><td>Easiness" + ": %1.2f</td></tr>" % card.easiness
            html += "<tr><td>Repetitions" + ": %d</td></tr>" % \
                (card.acq_reps + card.ret_reps)
            html += "<tr><td>Lapses" + ": %d</td></tr>" % card.lapses
            html += "<tr><td>Interval" + ": %d</td></tr>" % \
                (card.interval / DAY)
            html += "<tr><td>Last repetition" + ": %s</td></tr>" \
                % time.strftime("%B %d, %Y", time.gmtime(card.last_rep))
            html += "<tr><td>Next repetition" + ": %s</td></tr>" \
                % time.strftime("%B %d, %Y", time.gmtime(card.next_rep))
            html += "<tr><td>Average thinking time (secs): %d</td></tr>"\
                % self.database().average_thinking_time(card)
            html += "<tr><td>Total thinking time (secs): %d</td></tr>" \
                % self.database().total_thinking_time(card)
        html += "</table></body></html>"
        html = self.renderer.change_font_size(html)
        self.renderer.render_html(self.current_card_html_widget, html)
        self.mode_statistics_switcher.set_current_page(0)

    def common_statistics_cb(self, widget):
        """Switches to the common card statistics page."""

        html = self.html
        html += "<tr><td><b>Total cards statistics</b></td></tr>"
        html += "<tr><td>Total cards: %d<br><br><br></td></tr>" % \
            sum([self.database().card_count_for_grade(grade) \
            for grade in range(-1, 6)])
        html += "<tr><td><b>Grade statistics for all cards</b></td></tr>"
        for grade in range(-1, 6):
            html += "<tr><td>Grade %2i: %i cards</td></tr>" % \
                (grade, self.database().card_count_for_grade(grade))
        html += "</table></body></html>"
        html = self.renderer.change_font_size(html)
        self.renderer.render_html(self.total_card_html_widget, html)
        self.mode_statistics_switcher.set_current_page(1)
        
    def tags_statistics_cb(self, widget):
        """Switches to the tags statistics page."""

        html = self.html
        html += "<tr><td><b>Tags statistics<br></b></td></tr>"
        for _id, name in self.database().get_tags__id_and_name():
            html += "<tr><td><br><br>Tag <b>%s</b></td></tr>" % name
            for grade in range(-1, 6):
               html += "<tr><td>Grade %2i: %i cards</td></tr>" % (grade, \
                self.database().card_count_for_grade_and__tag_id(grade, _id))
        html += "</table></body></html>"
        html = self.renderer.change_font_size(html)
        self.renderer.render_html(self.tags_html_widget, html)
        self.mode_statistics_switcher.set_current_page(2)

