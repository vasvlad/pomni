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
Hildon UI. Widgets for review.
"""

import gtk
import mnemosyne.maemo_ui.widgets.common as widgets

def create_review_ui(main_switcher):
    """Creates ReviewWidget UI."""

    def create_button(name, width=80, height=80):
        button = gtk.Button()
        button.set_size_request(width, height)
        button.set_name(name)
        return button

    toplevel_table = gtk.Table(rows=1, columns=3)
    # create toolbar container   
    toolbar_container = gtk.Notebook()
    toolbar_container.set_show_tabs(False)
    toolbar_container.set_size_request(82, 480)
    toolbar_container.set_name('review_toolbar_container')
    # create grades container
    grades_container = gtk.Notebook()
    grades_container.set_show_tabs(False)
    grades_container.set_size_request(82, 480)
    grades_container.set_name('grades_container')
    widgets_table = gtk.Table(rows=2, columns=1)
    widgets_table.set_row_spacings(14)
    toolbar_table = gtk.Table(rows=5, columns=1, homogeneous=True)
    grades_table = gtk.Table(rows=6, columns=1, homogeneous=True)
    widgets_box = gtk.VBox(spacing=10)
    question_box = gtk.VBox(homogeneous=True)
    sound_container = gtk.Table(rows=1, columns=10, homogeneous=True)
    sound_button = gtk.Button()
    sound_button.set_name('media_button')
    # create tags label
    tags_label = gtk.Label()
    tags_label.set_name('tags_label')
    tags_label.set_justify(gtk.JUSTIFY_LEFT)
    tags_label.set_single_line_mode(True)
    answer_container = gtk.Frame()
    answer_container.set_name('html_container')
    question_container = gtk.Frame()
    question_container.set_name('html_container')
    answer_text = widgets.create_gtkhtml()
    question_text = widgets.create_gtkhtml()
    # create toolbar buttons
    buttons = {}
    buttons[0] = create_button('review_toolbar_tts_button')
    buttons[1] = create_button('review_toolbar_edit_card_button')
    buttons[2] = create_button('plus_button')
    buttons[3] = create_button('review_toolbar_stat_current_card_button')
    buttons[4] = create_button('review_toolbar_delete_card_button')
    buttons[5] = create_button('main_menu_button')
    # create grades buttons
    grades = {}
    for num in range(6):
        grades[num] = create_button('grade%s' % num)
    # packing toolbar buttons
    for pos in buttons.keys():
        toolbar_table.attach(buttons[pos], 0, 1, pos, pos + 1, \
            xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
    toolbar_container.add(toolbar_table)
    # packing grades buttons
    for pos in grades.keys():
        grades_table.attach(grades[pos], 0, 1, 5 - pos, 6 - pos, \
            xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
    grades_container.add(grades_table)
    toplevel_table.attach(toolbar_container, 0, 1, 0, 1, \
        xoptions=gtk.SHRINK, yoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL)
    toplevel_table.attach(grades_container, 3, 4, 0, 1, \
        xoptions=gtk.SHRINK, yoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL)
    question_container.add(question_text)
    answer_container.add(answer_text)
    sound_container.attach(sound_button, 3, 7, 0, 1, \
        xoptions=gtk.EXPAND|gtk.FILL|gtk.SHRINK, \
        yoptions=gtk.EXPAND|gtk.FILL|gtk.SHRINK)
    question_box.pack_start(sound_container)
    question_box.pack_end(question_container)
    widgets_box.pack_start(question_box)
    widgets_box.pack_end(answer_container)
    widgets_table.attach(tags_label, 0, 1, 0, 1, \
        xoptions=gtk.SHRINK, yoptions=gtk.SHRINK, xpadding=4)
    widgets_table.attach(widgets_box, 0, 1, 1, 2, \
        xoptions=gtk.SHRINK|gtk.FILL|gtk.EXPAND, \
        yoptions=gtk.SHRINK|gtk.FILL|gtk.EXPAND)
    toplevel_table.attach(widgets_table, 2, 3, 0, 1, ypadding=30,
        xoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL, \
        yoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL, xpadding=30)
    toplevel_table.show_all()
    # hide necessary widgets
    sound_container.hide()
    return main_switcher.append_page(toplevel_table), buttons[0], buttons[1], \
        buttons[4], question_container, answer_container, question_text, \
        answer_text, sound_container, sound_button, grades_table, \
        grades.values(), buttons.values(), tags_label


