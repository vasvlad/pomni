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
Hildon UI. UI factory.
"""

import gtk
import gtkhtml2
import urllib
import urlparse


def create_gtkhtml():
    """ Create gtkhtml2 widget """

    def request_url(document, url, stream):
        """Get content from url."""
        uri = urlparse.urljoin("", url)
        fpurl = urllib.FancyURLopener().open(uri)
        stream.write(fpurl.read())
        fpurl.close()
        stream.close()

    view = gtkhtml2.View()
    document = gtkhtml2.Document()
    document.connect('request_url', request_url)
    view.set_document(document)
    view.document = document
    view.show()
    return view


def create_main_ui():
    """Creates MainWidget UI."""

    window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    window.resize(800, 480)
    window.set_name('window')
    switcher = gtk.Notebook()
    switcher.set_show_border(False)
    switcher.set_show_tabs(False)
    window.add(switcher)
    return window, switcher


def create_menu_ui(main_switcher):
    """Creates MenuWidget UI."""

    toplevel_table = gtk.Table(rows=2, columns=1)
    app_name_label = gtk.Label('Mnemosyne for Maemo')
    app_name_label.set_name('program_name_label')
    buttons_table = gtk.Table(rows=2, columns=1)
    buttons_table.set_row_spacings(14)
    row1 = gtk.Table(rows=1, columns=5)
    row1.set_col_spacings(28)
    row2 = gtk.Table(rows=1, columns=5)
    row2.set_col_spacings(28)
    buttons = {}
    for button_name in ('tags', 'review', 'input', 'settings', \
        'statistics', 'about', 'exit'):
        button = gtk.Button()
        button.set_size_request(110, 155)
        button.set_name('menu_button_%s' % button_name)
        button_table = gtk.Table(rows=4, columns=1, homogeneous=True)
        button_label = gtk.Label(button_name.capitalize())
        button_label.set_name('menu_label_%s' % button_name)
        button_table.attach(button_label, 0, 1, 3, 4)
        button.add(button_table)
        buttons[button_name] = button
    # packing
    row1.attach(buttons['review'], 1, 2, 0, 1)
    row1.attach(buttons['input'], 2, 3, 0, 1)
    row1.attach(buttons['tags'], 3, 4, 0, 1)
    row2.attach(buttons['settings'], 1, 2, 0, 1)
#    row2.attach(buttons['sync'], 1, 2, 0, 1)
    row2.attach(buttons['statistics'], 2, 3, 0, 1)
    row2.attach(buttons['about'], 3, 4, 0, 1)
    row2.attach(buttons['exit'], 5, 6, 0, 1)
    buttons_table.attach(row1, 0, 1, 0, 1, xoptions=gtk.EXPAND, \
        yoptions=gtk.EXPAND)
    buttons_table.attach(row2, 0, 1, 1, 2, xoptions=gtk.EXPAND, \
        yoptions=gtk.EXPAND)
    toplevel_table.attach(app_name_label, 0, 1, 0, 1, \
        yoptions=gtk.SHRINK, ypadding=10)
    toplevel_table.attach(buttons_table, 0, 1, 1, 2, \
        xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
    toplevel_table.show_all()
    return main_switcher.append_page(toplevel_table), buttons


def create_tags_ui(main_switcher):
    """Creates TagsWidget UI."""

    toplevel_table = gtk.Table(rows=1, columns=2, homogeneous=False)
    # create toolbar container
    toolbar_container = gtk.Notebook()
    toolbar_container.set_show_tabs(False)
    toolbar_container.set_size_request(82, 420)
    toolbar_container.set_name('one_button_container')
    toolbar_table = gtk.Table(rows=5, columns=1, homogeneous=True)
    # create menu button
    menu_button = gtk.Button()
    menu_button.set_size_request(80, 80)
    menu_button.set_name('main_menu_button')
    # create tags frame
    tags_frame = gtk.Frame()
    tags_frame.set_name('html_container')
    tags_eventbox = gtk.EventBox()
    tags_eventbox.set_visible_window(True)
    tags_eventbox.set_name('viewport_widget')
    tags_scrolledwindow = gtk.ScrolledWindow()
    tags_scrolledwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    tags_scrolledwindow.set_name('scrolled_window')
    tags_viewport = gtk.Viewport()
    tags_viewport.set_shadow_type(gtk.SHADOW_NONE)
    tags_viewport.set_name('viewport_widget')
    tags_box = gtk.VBox()
    # packing widgets
    tags_viewport.add(tags_box)
    tags_scrolledwindow.add(tags_viewport)
    tags_eventbox.add(tags_scrolledwindow)
    tags_frame.add(tags_eventbox)
    toolbar_table.attach(menu_button, 0, 1, 4, 5, xoptions=gtk.EXPAND, \
        yoptions=gtk.EXPAND)
    toolbar_container.add(toolbar_table)
    toplevel_table.attach(toolbar_container, 0, 1, 0, 1, \
       xoptions=gtk.SHRINK, yoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL)
    toplevel_table.attach(tags_frame, 1, 2, 0, 1, \
        xoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL, \
        yoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL, \
        xpadding=30, ypadding=30)
    toplevel_table.show_all()
    return main_switcher.append_page(toplevel_table), tags_box, menu_button


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
    toolbar_container.set_name('toolbar_container')
    # create grades container
    grades_container = gtk.Notebook()
    grades_container.set_show_tabs(False)
    grades_container.set_size_request(82, 480)
    grades_container.set_name('grades_container')
    toolbar_table = gtk.Table(rows=5, columns=1, homogeneous=True)
    grades_table = gtk.Table(rows=6, columns=1, homogeneous=True)
    widgets_box = gtk.VBox(spacing=10)
    question_box = gtk.VBox(homogeneous=True)
    sound_container = gtk.Table(rows=1, columns=10, homogeneous=True)
    sound_button = gtk.Button()
    sound_button.set_name('media_button')
    answer_container = gtk.Frame()
    answer_container.set_name('html_container')
    question_container = gtk.Frame()
    question_container.set_name('html_container')
    answer_text = create_gtkhtml()
    question_text = create_gtkhtml()
    # create toolbar buttons
    buttons = {}
    buttons[0] = create_button('review_toolbar_tts_button')
    buttons[1] = create_button('review_toolbar_edit_card_button')
    buttons[2] = create_button('plus_button')
    buttons[3] = create_button('review_toolbar_delete_card_button')
    buttons[4] = create_button('main_menu_button') 
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
    toplevel_table.attach(widgets_box, 2, 3, 0, 1, ypadding=30,
        xoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL, \
        yoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL, xpadding=30)
    toplevel_table.show_all()
    # hide necessary widgets
    sound_container.hide()
    return main_switcher.append_page(toplevel_table), buttons[0], buttons[1], \
        buttons[3], question_container, answer_container, question_text, \
        answer_text, sound_container, sound_button, grades_table, \
        grades.values(), buttons.values()


def create_input_ui(main_switcher):
    """Creates InputWidget UI."""

    toplevel_table = gtk.Table(rows=1, columns=2)
    # create toolbar container
    toolbar_container = gtk.Notebook()
    toolbar_container.set_show_tabs(False)
    toolbar_container.set_size_request(82, 480)
    toolbar_container.set_name('toolbar_container')
    toolbar_table = gtk.Table(rows=5, columns=1, homogeneous=True)
    # create toolbar buttons
    card_type_button = gtk.Button()
    card_type_button.set_size_request(80, 80)
    content_button = gtk.Button()
    content_button.set_size_request(80, 80)
    add_card_button = gtk.Button()
    add_card_button.set_size_request(80, 80)
    add_card_button.set_name('plus_button')
    menu_button = gtk.Button()
    menu_button.set_size_request(80, 80)
    menu_button.set_name('main_menu_button')
    widgets_table = gtk.Table(rows=2, columns=1)
    widgets_table.set_row_spacings(14)
    tags_button = gtk.Button()
    tags_button.set_size_request(-1, 60)
    tags_button.set_name('tags_button')
    card_type_switcher = gtk.Notebook()
    card_type_switcher.set_show_tabs(False)
    card_type_switcher.set_show_border(False)
    two_sided_box = gtk.VBox(spacing=10)
    sound_box = gtk.VBox()
    sound_box.set_homogeneous(True)
    sound_container = gtk.Table(rows=1, columns=3, homogeneous=True)
    sound_button = gtk.ToggleButton()
    sound_button.set_name('media_button')
    # create text fields
    question_container = gtk.Frame()
    question_container.set_name('html_container')
    question_text = gtk.TextView()
    question_text.set_name('textview_widget')
    question_text.set_justification(gtk.JUSTIFY_CENTER)
    question_text.set_wrap_mode(gtk.WRAP_WORD)
    answer_container = gtk.Frame()
    answer_container.set_name('html_container')
    answer_text = gtk.TextView()
    answer_text.set_name('textview_widget')
    answer_text.set_justification(gtk.JUSTIFY_CENTER)
    answer_text.set_wrap_mode(gtk.WRAP_WORD)
    three_sided_box = gtk.VBox(spacing=10)
    foreign_container = gtk.Frame()
    foreign_container.set_name('html_container')
    foreign_text = gtk.TextView()
    foreign_text.set_name('textview_widget')
    foreign_text.set_justification(gtk.JUSTIFY_CENTER)
    foreign_text.set_wrap_mode(gtk.WRAP_WORD)
    pronunciation_container = gtk.Frame()
    pronunciation_container.set_name('html_container')
    pronunciation_text = gtk.TextView()
    pronunciation_text.set_name('textview_widget')
    pronunciation_text.set_justification(gtk.JUSTIFY_CENTER)
    pronunciation_text.set_wrap_mode(gtk.WRAP_WORD)
    translation_container = gtk.Frame()
    translation_container.set_name('html_container')
    translation_text = gtk.TextView()
    translation_text.set_name('textview_widget')
    translation_text.set_justification(gtk.JUSTIFY_CENTER)
    translation_text.set_wrap_mode(gtk.WRAP_WORD)
    cloze_box = gtk.VBox()
    cloze_container = gtk.Frame()
    cloze_container.set_name('html_container')
    cloze_text = gtk.TextView()
    cloze_text.set_name('textview_widget')
    cloze_text.set_justification(gtk.JUSTIFY_CENTER)
    cloze_text.set_wrap_mode(gtk.WRAP_WORD)
    # create new tag elements
    tags_layout = gtk.VBox(spacing=26)
    new_tag_box = gtk.HBox()
    new_tag_label = gtk.Label()
    new_tag_label.set_text('New tag: ')
    new_tag_label.set_name('white_label')
    new_tag_button = gtk.Button()
    new_tag_button.set_size_request(60, 60)
    new_tag_button.set_name('plus_button')
    new_tag_frame = gtk.Frame()
    new_tag_frame.set_name('html_container')
    new_tag_entry = gtk.Entry()
    new_tag_entry.set_name('entry_widget')
    # creates 'tags list' elements
    tags_frame = gtk.Frame()
    tags_frame.set_name('html_container')
    tags_eventbox = gtk.EventBox()
    tags_eventbox.set_visible_window(True)
    tags_eventbox.set_name('viewport_widget')
    tags_scrolledwindow = gtk.ScrolledWindow()
    tags_scrolledwindow.set_policy(gtk.POLICY_AUTOMATIC, \
        gtk.POLICY_AUTOMATIC)
    tags_scrolledwindow.set_name('scrolled_window')
    tags_viewport = gtk.Viewport()
    tags_viewport.set_name('viewport_widget')
    tags_viewport.set_shadow_type(gtk.SHADOW_NONE)
    tags_box = gtk.VBox()
    tags_box.set_homogeneous(True)
    # packing widgets
    toolbar_table.attach(card_type_button, 0, 1, 0, 1, \
        xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
    toolbar_table.attach(content_button, 0, 1, 1, 2, \
        xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
    toolbar_table.attach(add_card_button, 0, 1, 2, 3, \
        xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
    toolbar_table.attach(menu_button, 0, 1, 4, 5, \
        xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
    toolbar_container.add(toolbar_table)
    toplevel_table.attach(toolbar_container, 0, 1, 0, 1, \
        xoptions=gtk.SHRINK, yoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL)
    widgets_table.attach(tags_button, 0, 1, 0, 1, \
        xoptions=gtk.SHRINK|gtk.FILL|gtk.EXPAND, \
        yoptions=gtk.SHRINK, xpadding=4)
    widgets_table.attach(card_type_switcher, 0, 1, 1, 2, \
        xoptions=gtk.SHRINK|gtk.FILL|gtk.EXPAND, \
        yoptions=gtk.SHRINK|gtk.FILL|gtk.EXPAND)
    card_type_switcher.append_page(two_sided_box)
    card_type_switcher.append_page(three_sided_box)
    card_type_switcher.append_page(cloze_box)
    card_type_switcher.append_page(tags_layout)
    sound_container.attach(sound_button, 1, 2, 0, 1, \
        xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL|gtk.SHRINK)
    question_container.add(question_text)
    sound_box.pack_start(sound_container)
    sound_box.pack_end(question_container)
    answer_container.add(answer_text)
    two_sided_box.pack_start(sound_box)
    two_sided_box.pack_end(answer_container)
    foreign_container.add(foreign_text)
    pronunciation_container.add(pronunciation_text)
    translation_container.add(translation_text)
    three_sided_box.pack_start(foreign_container)
    three_sided_box.pack_start(pronunciation_container)
    three_sided_box.pack_end(translation_container)
    cloze_container.add(cloze_text)
    cloze_box.pack_start(cloze_container)
    new_tag_frame.add(new_tag_entry)
    new_tag_box.pack_start(new_tag_label, expand=False, fill=False, padding=10)
    new_tag_box.pack_start(new_tag_frame, expand=True, fill=True, padding=10)
    new_tag_box.pack_end(new_tag_button, expand=False, fill=False)
    tags_viewport.add(tags_box)
    tags_scrolledwindow.add(tags_viewport)
    tags_eventbox.add(tags_scrolledwindow)
    tags_frame.add(tags_eventbox)
    tags_layout.pack_start(new_tag_box, expand=False, fill=False)
    tags_layout.pack_end(tags_frame, expand=True, fill=True)
    toplevel_table.attach(widgets_table, 1, 2, 0, 1, \
        xoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL, xpadding=30, \
        yoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL, ypadding=30)
    toplevel_table.show_all()
    # hide necessary widgets
    sound_container.hide()
    return main_switcher.append_page(toplevel_table), card_type_button, \
        content_button, menu_button, tags_button, sound_button, question_text, \
        answer_text, foreign_text, pronunciation_text, translation_text, \
        cloze_text, new_tag_button, new_tag_entry, tags_box, \
        card_type_switcher, add_card_button, sound_container, \
        question_container, toolbar_container


def create_configuration_ui(main_switcher):
    """Creates ConfigureWidget UI."""

    toplevel_table = gtk.Table(rows=1, columns=2)
    toolbar_container = create_toolbar_container('toolbar_container')
    toolbar_table = gtk.Table(rows=5, columns=1, homogeneous=True)
    general_settings_button = create_radio_button(None, \
        'config_toolbar_general_settings_button', None, width=80, height=80)
    skin_settings_button = create_radio_button(general_settings_button, 
        'config_toolbar_skin_settings_button', None, width=80, height=80)
    tts_settings_button = create_radio_button(general_settings_button,
        'config_toolbar_tts_settings_button', None, width=80, height=80)
    menu_button = create_button('main_menu_button', None)
    mode_settings_switcher = gtk.Notebook()
    mode_settings_switcher.set_show_tabs(False)
    mode_settings_switcher.set_show_border(False)
    mode_settings_switcher.set_name('config_mode_settings_switcher')
    general_settings_table = gtk.Table(rows=2, columns=1, homogeneous=True)
    general_settings_table.set_row_spacings(10)
    directories_table = gtk.Table(rows=2, columns=1, homogeneous=True)
    directories_table.set_row_spacings(12)
    sounddir_box = gtk.VBox()
    sounddir_box.set_spacing(1)
    sounddir_label_container = gtk.HBox()
    sounddir_label = gtk.Label('  Sound directory:')
    sounddir_label.set_name('white_label')
    sounddir_container = gtk.Frame()
    sounddir_container.set_name('html_container')
    sounddir_entry = gtk.Entry()
    sounddir_entry.set_name('entry_widget')
    imagedir_box = gtk.VBox()
    imagedir_box.set_spacing(1)
    imagedir_label_container = gtk.HBox()
    imagedir_label = gtk.Label('  Image directory:')
    imagedir_label.set_name('white_label')
    imagedir_container = gtk.Frame()
    imagedir_container.set_name('html_container')
    imagedir_entry = gtk.Entry()
    imagedir_entry.set_name('entry_widget')
    checkboxes_box = gtk.VBox(homogeneous=True)
    checkboxes_box.set_spacing(12)
    fullscreen_table = gtk.Table(rows=1, columns=2)
    fullscreen_table.set_col_spacings(10)
    fullscreen_checkbox = gtk.ToggleButton()
    fullscreen_checkbox.set_size_request(64, 64)
    fullscreen_checkbox.set_name('config_checkbox')
    fullscreen_label = gtk.Label('Start in Fullscreen mode')
    fullscreen_label.set_name('white_label')
    start_with_review_table = gtk.Table(rows=1, columns=2)
    start_with_review_table.set_col_spacings(10)
    start_with_review_checkbox = gtk.ToggleButton()
    start_with_review_checkbox.set_size_request(64, 64)
    start_with_review_checkbox.set_name('config_checkbox')
    start_with_review_label = gtk.Label('Open Review mode at startup')
    start_with_review_label.set_name('white_label')
    skin_settings_table = gtk.Table(rows=1, columns=1)
    font_size_table = gtk.Table(rows=1, columns=3)
    font_size_example_container = gtk.Frame()
    font_size_example_container.set_size_request(-1, 140)
    font_size_example_container.set_name('html_container')
    font_size = create_gtkhtml()
    font_size_decrease_button = create_button('down_arrow', None, \
        width=64, height=64)
    font_size_increase_button = create_button('up_arrow', None, width=64, \
        height=64)
    tts_settings_table = gtk.Table(rows=2, columns=1, homogeneous=True)
    tts_settings_table1 = gtk.Table(rows=2, columns=1, homogeneous=True)
    tts_settings_table1.set_row_spacings(10)
    tts_lang_table = gtk.Table(rows=1, columns=3)
    tts_lang_container = create_button('labels_container', width=-1, height=60)
    tts_lang_label = gtk.Label('default')
    tts_lang_label.set_name('config_tts_label')
    tts_lang_prev_button = create_button('main_menu_button', \
        None)
    tts_lang_next_button = create_button('right_arrow', None)
    tts_voice_table = gtk.Table(rows=1, columns=3)
    tts_voice_container = create_button('labels_container', width=-1, height=60)
    tts_voice_label = gtk.Label('Male')
    tts_voice_label.set_name('config_tts_label')
    tts_voice_prev_button = create_button('main_menu_button', \
        None)
    tts_voice_next_button = create_button('right_arrow', None)
    tts_settings_table2 = gtk.Table(rows=2, columns=1, homogeneous=True)
    tts_settings_table2.set_row_spacings(10)
    tts_speed_box = gtk.VBox()
    tts_speed_box.set_spacing(10)
    tts_speed_label_box = gtk.HBox()
    tts_speed_label = gtk.Label('Speed:')
    tts_speed_label.set_name('config_scrollbar_label')
    tts_speed_scrollbar = gtk.HScrollbar()
    tts_speed_scrollbar.set_adjustment(gtk.Adjustment(lower=30, upper=200))
    tts_speed_scrollbar.set_increments(step=1, page=10)
    tts_speed_scrollbar.set_update_policy(gtk.UPDATE_CONTINUOUS)
    tts_speed_scrollbar.set_name('config_scrollbar')
    tts_pitch_box = gtk.VBox()
    tts_pitch_box.set_spacing(10)
    tts_pitch_label_box = gtk.HBox()
    tts_pitch_label = gtk.Label('Pitch:')
    tts_pitch_label.set_name('config_scrollbar_label')
    tts_pitch_scrollbar = gtk.HScrollbar()
    tts_pitch_scrollbar.set_update_policy(gtk.UPDATE_CONTINUOUS)
    tts_pitch_scrollbar.set_adjustment(gtk.Adjustment(lower=0, upper=100))
    tts_pitch_scrollbar.set_increments(step=1, page=10)
    tts_pitch_scrollbar.set_name('config_scrollbar')
    # packing widgets
    toolbar_table.attach(general_settings_button, 0, 1, 0, 1, \
        xoptions=gtk.SHRINK, yoptions=gtk.EXPAND)
    toolbar_table.attach(skin_settings_button, 0, 1, 1, 2, \
        xoptions=gtk.SHRINK, yoptions=gtk.EXPAND)
    toolbar_table.attach(tts_settings_button, 0, 1, 2, 3, \
        xoptions=gtk.SHRINK, yoptions=gtk.EXPAND)
    toolbar_table.attach(menu_button, 0, 1, 4, 5, \
        xoptions=gtk.SHRINK, yoptions=gtk.EXPAND)
    toolbar_container.add(toolbar_table)
    toplevel_table.attach(toolbar_container, 0, 1, 0, 1, \
        xoptions=gtk.SHRINK, yoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL)
    imagedir_container.add(imagedir_entry)
    imagedir_label_container.pack_start(imagedir_label, expand=False, 
        fill=False)
    imagedir_box.pack_start(imagedir_label_container)
    imagedir_box.pack_end(imagedir_container)
    sounddir_container.add(sounddir_entry)
    sounddir_label_container.pack_start(sounddir_label, expand=False, \
        fill=False)
    sounddir_box.pack_start(sounddir_label_container)
    sounddir_box.pack_end(sounddir_container)
    directories_table.attach(sounddir_box, 0, 1, 0, 1, xpadding=14, \
        xoptions=gtk.EXPAND|gtk.FILL|gtk.SHRINK, \
        yoptions=gtk.EXPAND|gtk.SHRINK)
    directories_table.attach(imagedir_box, 0, 1, 1, 2, xpadding=14, \
        xoptions=gtk.EXPAND|gtk.FILL|gtk.SHRINK, \
        yoptions=gtk.EXPAND|gtk.SHRINK)
    start_with_review_table.attach(start_with_review_checkbox, 0, 1, 0, 1, \
        xoptions=gtk.SHRINK, yoptions=gtk.EXPAND|gtk.FILL)
    start_with_review_table.attach(start_with_review_label, 1, 2, 0, 1, \
        xoptions=gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL)
    fullscreen_table.attach(fullscreen_checkbox, 0, 1, 0, 1, \
        xoptions=gtk.SHRINK, yoptions=gtk.EXPAND|gtk.SHRINK)
    fullscreen_table.attach(fullscreen_label, 1, 2, 0, 1, \
        xoptions=gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL)
    checkboxes_box.pack_start(fullscreen_table)
    checkboxes_box.pack_end(start_with_review_table)
    general_settings_table.attach(directories_table, 0, 1, 0, 1, \
        xoptions=gtk.EXPAND|gtk.FILL|gtk.SHRINK, ypadding=10, 
        yoptions=gtk.EXPAND|gtk.FILL|gtk.SHRINK)
    general_settings_table.attach(checkboxes_box, 0, 1, 1, 2, \
        xoptions=gtk.EXPAND|gtk.FILL|gtk.SHRINK, xpadding=13, \
        yoptions=gtk.EXPAND|gtk.SHRINK)
    mode_settings_switcher.append_page(general_settings_table)
    font_size_example_container.add(font_size)
    font_size_table.attach(font_size_decrease_button, 0, 1, 0, 1, \
        xoptions=gtk.SHRINK, yoptions=gtk.EXPAND)
    font_size_table.attach(font_size_example_container, 1, 2, 0, 1, \
        xoptions=gtk.EXPAND|gtk.FILL, xpadding=14, \
        yoptions=gtk.EXPAND|gtk.FILL|gtk.SHRINK)
    font_size_table.attach(font_size_increase_button, 2, 3, 0, 1, \
        xoptions=gtk.SHRINK, yoptions=gtk.EXPAND)
    skin_settings_table.attach(font_size_table, 0, 1, 0, 1, \
        xoptions=gtk.EXPAND|gtk.FILL|gtk.SHRINK, yoptions=gtk.EXPAND)
    mode_settings_switcher.append_page(skin_settings_table)
    tts_voice_container.add(tts_voice_label)
    tts_voice_table.attach(tts_voice_prev_button, 0, 1, 0, 1, \
        xoptions=gtk.SHRINK, yoptions=gtk.EXPAND)
    tts_voice_table.attach(tts_voice_container, 1, 2, 0, 1, \
        xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.SHRINK)
    tts_voice_table.attach(tts_voice_next_button, 2, 3, 0, 1, \
        xoptions=gtk.SHRINK, yoptions=gtk.EXPAND)
    tts_lang_container.add(tts_lang_label)
    tts_lang_table.attach(tts_lang_prev_button, 0, 1, 0, 1, \
        xoptions=gtk.SHRINK, yoptions=gtk.EXPAND)
    tts_lang_table.attach(tts_lang_container, 1, 2, 0, 1, \
        xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.SHRINK)
    tts_lang_table.attach(tts_lang_next_button, 2, 3, 0, 1, \
        xoptions=gtk.SHRINK, yoptions=gtk.EXPAND)
    tts_speed_label_box.pack_start(tts_speed_label, expand=False, fill=False)
    tts_speed_box.pack_start(tts_speed_label_box, expand=False, fill=False)
    tts_speed_box.pack_end(tts_speed_scrollbar)
    tts_pitch_label_box.pack_start(tts_pitch_label, expand=False, fill=False)
    tts_pitch_box.pack_start(tts_pitch_label_box, expand=False, fill=False)
    tts_pitch_box.pack_end(tts_pitch_scrollbar)
    tts_settings_table2.attach(tts_speed_box, 0, 1, 0, 1, \
        xoptions=gtk.EXPAND|gtk.FILL|gtk.SHRINK, \
        yoptions=gtk.EXPAND|gtk.FILL|gtk.SHRINK)
    tts_settings_table2.attach(tts_pitch_box, 0, 1, 1, 2, \
        xoptions=gtk.EXPAND|gtk.FILL|gtk.SHRINK, \
        yoptions=gtk.EXPAND|gtk.FILL|gtk.SHRINK)
    tts_settings_table1.attach(tts_lang_table, 0, 1, 0, 1, \
        xoptions=gtk.EXPAND|gtk.FILL|gtk.SHRINK, \
        yoptions=gtk.EXPAND|gtk.FILL|gtk.SHRINK)
    tts_settings_table1.attach(tts_voice_table, 0, 1, 1, 2, \
        xoptions=gtk.EXPAND|gtk.FILL|gtk.SHRINK, \
        yoptions=gtk.EXPAND|gtk.FILL|gtk.SHRINK)
    tts_settings_table.attach(tts_settings_table1, 0, 1, 0, 1, \
        xoptions=gtk.EXPAND|gtk.FILL|gtk.SHRINK, \
        yoptions=gtk.EXPAND|gtk.FILL|gtk.SHRINK)
    tts_settings_table.attach(tts_settings_table2, 0, 1, 1, 2, \
        xoptions=gtk.EXPAND|gtk.FILL|gtk.SHRINK, \
        yoptions=gtk.EXPAND|gtk.FILL|gtk.SHRINK)
    mode_settings_switcher.append_page(tts_settings_table)
    toplevel_table.attach(mode_settings_switcher, 1, 2, 0, 1, \
        xoptions=gtk.EXPAND|gtk.FILL|gtk.SHRINK, xpadding = 14, \
        yoptions=gtk.EXPAND|gtk.FILL|gtk.SHRINK, ypadding=14)
    toplevel_table.show_all()
    return main_switcher.append_page(toplevel_table), tts_settings_button, \
        general_settings_button, skin_settings_button, mode_settings_switcher,\
        fullscreen_checkbox, start_with_review_checkbox, imagedir_entry, \
        sounddir_entry, tts_voice_label, tts_pitch_label, tts_lang_label, \
        tts_speed_label, tts_speed_scrollbar, tts_pitch_scrollbar, font_size, \
        tts_lang_prev_button, tts_lang_next_button, menu_button, \
        font_size_decrease_button, font_size_increase_button, \
        tts_voice_prev_button, tts_voice_next_button


def create_sync_ui(main_switcher):
    """Creates SyncWidget UI."""

    toplevel_table = gtk.Table(rows=1, columns=2)
    toolbar_container = gtk.Notebook()
    toolbar_container.set_show_tabs(False)
    toolbar_container.set_size_request(82, 480)
    toolbar_container.set_name('three_button_container')
    toolbar_table = gtk.Table(rows=5, columns=1, homogeneous=True)
    client_mode_button = gtk.ToggleButton()
    client_mode_button.set_size_request(80, 80)
    client_mode_button.set_name('sync_toolbar_client_mode_button')
    server_mode_button = gtk.ToggleButton()
    server_mode_button.set_size_request(80, 80)
    server_mode_button.set_name('sync_toolbar_server_mode_button')
    menu_button = create_button('main_menu_button')
    role_switcher = gtk.Notebook()
    role_switcher.set_show_tabs(False)
    role_switcher.set_show_border(False)
    information_label = gtk.Label('This mode allows you to sync your ' \
        'database with another copy of Mnemosyne program. You can use it' \
        'as Server or Client.')
    information_label.set_line_wrap(True)
    information_label.set_justify(gtk.JUSTIFY_CENTER)
    information_label.set_name('white_label')
    client_table = gtk.Table(rows=2, columns=1)
    server_table = gtk.Table(rows=2, columns=1)
    client_start_button = gtk.ToggleButton()
    client_start_button.set_size_request(72, 72)
    client_start_button.set_name('sync_button')
    server_start_button = gtk.ToggleButton()
    server_start_button.set_size_request(72, 72)
    server_start_button.set_name('sync_button')
    client_box = gtk.VBox()
    client_params_table = gtk.Table(rows=4, columns=2)
    client_params_table.set_row_spacings(10)
    client_params_table.set_col_spacings(10)
    client_status_table = gtk.VBox()
    client_status_label = gtk.Label()
    client_status_label.set_name('white_label')
    client_progressbar = gtk.ProgressBar()
    client_progressbar.set_name('sync_mode_client_progressbar')
    client_login_label = gtk.Label('Login:')
    client_login_label.set_name('white_label')
    client_passwd_label = gtk.Label('Password:')
    client_passwd_label.set_name('white_label')
    client_address_label = gtk.Label('Server address:')
    client_address_label.set_name('white_label')
    client_port_label = gtk.Label('Server port:')
    client_port_label.set_name('white_label')
    client_login_entry_container = gtk.Frame()
    client_login_entry_container.set_name('html_container')
    client_passwd_entry_container = gtk.Frame()
    client_passwd_entry_container.set_name('html_container')
    client_address_entry_container = gtk.Frame()
    client_address_entry_container.set_name('html_container')
    client_port_entry_container = gtk.Frame()
    client_port_entry_container.set_name('html_container')
    client_login_entry = gtk.Entry()
    client_login_entry.set_name('entry_widget')
    client_passwd_entry = gtk.Entry()
    client_passwd_entry.set_name('entry_widget')
    client_address_entry = gtk.Entry()
    client_address_entry.set_name('entry_widget')
    client_port_entry = gtk.Entry()
    client_port_entry.set_name('entry_widget')
    server_box = gtk.VBox()
    server_params_table = gtk.Table(rows=4, columns=2)
    server_params_table.set_row_spacings(10)
    server_params_table.set_col_spacings(10)
    server_status_table = gtk.VBox()
    server_status_label = gtk.Label()
    server_status_label.set_name('white_label')
    server_progressbar = gtk.ProgressBar()
    server_progressbar.set_name('sync_mode_server_progressbar')
    server_login_label = gtk.Label('Login:')
    server_login_label.set_name('white_label')
    server_passwd_label = gtk.Label('Password:')
    server_passwd_label.set_name('white_label')
    server_address_label = gtk.Label('IP address:')
    server_address_label.set_name('white_label')
    server_port_label = gtk.Label('Port:')
    server_port_label.set_name('white_label')
    server_login_entry_container = gtk.Frame()
    server_login_entry_container.set_name('html_container')
    server_passwd_entry_container = gtk.Frame()
    server_passwd_entry_container.set_name('html_container')
    server_address_entry_container = gtk.Frame()
    server_address_entry_container.set_name('html_container')
    server_port_entry_container = gtk.Frame()
    server_port_entry_container.set_name('html_container')
    server_login_entry = gtk.Entry()
    server_login_entry.set_name('entry_widget')
    server_passwd_entry = gtk.Entry()
    server_passwd_entry.set_name('entry_widget')
    server_address_entry = gtk.Entry()
    server_address_entry.set_name('entry_widget')
    server_port_entry = gtk.Entry()
    server_port_entry.set_name('entry_widget')
    # packing widgets
    toolbar_table.attach(client_mode_button, 0, 1, 0, 1, \
        xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
    toolbar_table.attach(server_mode_button, 0, 1, 1, 2, \
        xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
    toolbar_table.attach(menu_button, 0, 1, 4, 5, \
        xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
    toolbar_container.add(toolbar_table)
    toplevel_table.attach(toolbar_container, 0, 1, 0, 1, \
        xoptions=gtk.SHRINK, yoptions=gtk.EXPAND|gtk.FILL|gtk.SHRINK)
    role_switcher.append_page(information_label)
    client_login_entry_container.add(client_login_entry)
    client_passwd_entry_container.add(client_passwd_entry)
    client_address_entry_container.add(client_address_entry)
    client_port_entry_container.add(client_port_entry)
    client_params_table.attach(client_login_label, 0, 1, 0, 1, \
        xoptions=gtk.SHRINK, yoptions=gtk.SHRINK)
    client_params_table.attach(client_login_entry_container, 1, 2, 0, 1, \
        xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL)
    client_params_table.attach(client_passwd_label, 0, 1, 1, 2, \
        xoptions=gtk.SHRINK, yoptions=gtk.SHRINK)
    client_params_table.attach(client_passwd_entry_container, 1, 2, 1, 2, \
        xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL)
    client_params_table.attach(client_address_label, 0, 1, 2, 3, \
        xoptions=gtk.SHRINK, yoptions=gtk.SHRINK)
    client_params_table.attach(client_address_entry_container, 1, 2, 2, 3, \
        xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL)
    client_params_table.attach(client_port_label, 0, 1, 3, 4, \
        xoptions=gtk.SHRINK, yoptions=gtk.SHRINK)
    client_params_table.attach(client_port_entry_container, 1, 2, 3, 4, \
        xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL)
    client_status_table.pack_start(client_status_label, expand=False, \
        fill=False)
    client_status_table.pack_end(client_progressbar, expand=False, \
        fill=False)
    client_box.pack_start(client_params_table, expand=False, fill=True)
    client_box.pack_end(client_status_table, expand=True, fill=True)
    client_table.attach(client_start_button, 0, 1, 1, 2, \
        xoptions=gtk.EXPAND, yoptions=gtk.SHRINK, ypadding=4)
    client_table.attach(client_box, 0, 1, 0, 1, \
        xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL)
    role_switcher.append_page(client_table)
    server_login_entry_container.add(server_login_entry)
    server_passwd_entry_container.add(server_passwd_entry)
    server_address_entry_container.add(server_address_entry)
    server_port_entry_container.add(server_port_entry)
    server_params_table.attach(server_login_label, 0, 1, 0, 1, \
        xoptions=gtk.SHRINK, yoptions=gtk.SHRINK)
    server_params_table.attach(server_login_entry_container, 1, 2, 0, 1, \
        xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL)
    server_params_table.attach(server_passwd_label, 0, 1, 1, 2, \
        xoptions=gtk.SHRINK, yoptions=gtk.SHRINK)
    server_params_table.attach(server_passwd_entry_container, 1, 2, 1, 2, \
        xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL)
    server_params_table.attach(server_address_label, 0, 1, 2, 3, \
        xoptions=gtk.SHRINK, yoptions=gtk.SHRINK)
    server_params_table.attach(server_address_entry_container, 1, 2, 2, 3, \
        xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL)
    server_params_table.attach(server_port_label, 0, 1, 3, 4, \
        xoptions=gtk.SHRINK, yoptions=gtk.SHRINK)
    server_params_table.attach(server_port_entry_container, 1, 2, 3, 4, \
        xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL)
    server_status_table.pack_start(server_status_label, expand=False, \
        fill=False)
    server_status_table.pack_end(server_progressbar, expand=False, \
        fill=False)
    server_box.pack_start(server_params_table, expand=False, fill=True)
    server_box.pack_end(server_status_table, expand=True, fill=True)
    server_table.attach(server_start_button, 0, 1, 1, 2, \
        xoptions=gtk.EXPAND, yoptions=gtk.SHRINK, ypadding=4)
    server_table.attach(server_box, 0, 1, 0, 1, \
        xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL)
    role_switcher.append_page(server_table)
    toplevel_table.attach(role_switcher, 1, 2, 0, 1, xpadding=14, \
        ypadding=14, xoptions=gtk.EXPAND|gtk.FILL|gtk.SHRINK, \
        yoptions=gtk.EXPAND|gtk.FILL|gtk.SHRINK)
    toplevel_table.show_all()
    # hide necessary widgets
    client_status_table.hide()
    server_status_table.hide()
    return main_switcher.append_page(toplevel_table), client_progressbar, \
        server_progressbar, client_start_button, server_start_button, \
        role_switcher, client_mode_button, server_mode_button, \
        client_status_label, server_status_label, client_login_entry, \
        client_passwd_entry, client_address_entry, client_port_entry, \
        server_login_entry, server_passwd_entry, server_address_entry, \
        server_port_entry, menu_button, client_params_table, \
        server_params_table


def create_about_ui(main_switcher, image_name):
    """Creates AboutWidget UI."""

    toplevel_table = gtk.Table(rows=1, columns=2)
    toolbar_container = gtk.Notebook()
    toolbar_container.set_show_tabs(False)
    toolbar_container.set_size_request(82, 480)
    toolbar_container.set_name('one_button_container')
    toolbar_table = gtk.Table(rows=5, columns=1, homogeneous=True)
    menu_button = gtk.Button()
    menu_button.set_size_request(80, 80)
    menu_button.set_name('main_menu_button')
    info_container = gtk.Notebook()
    info_container.set_show_border(False)
    info_container.set_show_tabs(False)
    info_box = gtk.VBox()
    hbutton_box = gtk.HButtonBox()
    text_box = gtk.HBox()
    logo_box = gtk.HBox()
    label_left = gtk.Label()
    label_left.set_use_markup(True)
    label_left.set_markup("<span foreground='white' size='small'><b>" \
        "Developers:</b></span>\n<span foreground='white' size='small'>" \
        "Max Usachev |</span> <span foreground='#299BFC' size='small'>" \
        "maxusachev@gmail.com</span>\n<span foreground='white' size=" \
        "'small'>Ed Bartosh |</span> <span foreground='#299BFC' size=" \
        "'small'>bartosh@gmail.com</span>\n<span foreground='white' " \
        "size='small'>Vlad Vasiliev |</span> <span foreground='#299BFC' " \
        "size='small'>vlad@gas.by</span>\n\n<span foreground='white' " \
        "size='small'><b>Designer:</b>\n</span><span foreground='white' " \
        "size='small'>Andrew Zhilin |</span> <span foreground='#299BFC' " \
        "size='small'>drew.zhilin@gmail.com</span>\n\n<span foreground=" \
        "'white' size='small'><b>Development team:</b></span>\n<span " \
        "foreground='#299BFC' size='small'>pomni@googlegroups.com</span>")
    label_right = gtk.Label()
    label_right.set_use_markup(True)
    label_right.set_markup("<span foreground='white' size='small'><b>" \
        "Special Thanks To:</b></span>\n<span foreground='white' size=" \
        "'small'>Peter Bienstman</span>\n<span foreground='#299BFC' size=" \
        "'small'>Peter.Bienstman@ugent.be</span>\n<span foreground=" \
        "'#299BFC' size='small'>http://www.mnemosyne-proj.org/</span>" \
        "\n<span size='x-large'></span><span foreground='white' size=" \
        "'small'>\nGSoC 2009</span>\n<span foreground='#299BFC' size='"\
        "small'>http://socghop.appspot.com/</span>\n\n<span size='x-large'>" \
        "</span><span foreground='white' size='small'>\nMaemo community" \
        "</span>\n<span foreground='#299BFC' size='small'>" \
        "http://maemo.org/</span>")
    logo = gtk.Image()
    logo.set_from_file(image_name)
    program_label = gtk.Label()
    program_label.set_justify(gtk.JUSTIFY_CENTER)
    program_label.set_use_markup(True)
    program_label.set_markup("<span foreground='white' size='large'><b>" \
        "Mnemosyne for Maemo</b></span>\n<span foreground='white' size=" \
        "'large'>version 2.0.0 beta5</span>")
    # packing widgets
    logo_box.pack_start(logo, expand=False, fill=False, padding=10)
    logo_box.pack_end(program_label, expand=False, fill=False)
    hbutton_box.pack_start(logo_box)
    text_box.pack_start(label_left)
    text_box.pack_end(label_right)
    info_box.pack_start(hbutton_box, expand=False)
    info_box.pack_end(text_box)
    info_container.append_page(info_box)
    toolbar_table.attach(menu_button, 0, 1, 4, 5, xoptions=gtk.EXPAND, \
        yoptions=gtk.EXPAND)
    toolbar_container.append_page(toolbar_table)
    toplevel_table.attach(toolbar_container, 0, 1, 0, 1, \
        xoptions=gtk.SHRINK, yoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL)
    toplevel_table.attach(info_container, 1, 2, 0, 1, \
        xoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL, \
        yoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL)
    toplevel_table.show_all()
    return main_switcher.append_page(toplevel_table), menu_button

def create_statistics_ui(main_switcher, image_name):
    """Creates MaemoStatisticsWidget UI."""

    toplevel_table = gtk.Table(rows=1, columns=2)
    toolbar_container = gtk.Notebook()
    toolbar_container.set_show_tabs(False)
    toolbar_container.set_size_request(82, 480)
    toolbar_container.set_name('one_button_container')
    toolbar_table = gtk.Table(rows=5, columns=1, homogeneous=True)
    menu_button = gtk.Button()
    menu_button.set_size_request(80, 80)
    menu_button.set_name('main_menu_button')
    info_container = gtk.Notebook()
    info_container.set_show_border(False)
    info_container.set_show_tabs(False)
    info_box = gtk.VBox()
    info_container.append_page(info_box)
    toolbar_table.attach(menu_button, 0, 1, 4, 5, xoptions=gtk.EXPAND, \
        yoptions=gtk.EXPAND)
    toolbar_container.append_page(toolbar_table)
    toplevel_table.attach(toolbar_container, 0, 1, 0, 1, \
        xoptions=gtk.SHRINK, yoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL)
    toplevel_table.attach(info_container, 1, 2, 0, 1, \
        xoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL, \
        yoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL)
    toplevel_table.show_all()
    return main_switcher.append_page(toplevel_table), menu_button



def create_media_dialog_ui():
    """Creates MediaDialog UI."""

    def enable_select_button_cb(widget, select_button):
        """If user has select item - enable Select button."""
        select_button.set_sensitive(True)

    #liststore = [text, type, filename, dirname, pixbuf]
    liststore = gtk.ListStore(str, str, str, str, gtk.gdk.Pixbuf)
    dialog = gtk.Dialog()
    dialog.set_decorated(False)
    dialog.set_has_separator(False)
    dialog.resize(570, 410)
    width, height = dialog.get_size()
    dialog.move((gtk.gdk.screen_width() - width)/2, \
        (gtk.gdk.screen_height() - height)/2)
    iconview_widget = gtk.IconView()
    iconview_widget.set_name('iconview_widget')
    iconview_widget.set_model(liststore)
    iconview_widget.set_pixbuf_column(4)
    iconview_widget.set_text_column(0)
    label = gtk.Label('Select media')
    label.set_name('white_label')
    scrolledwindow_widget = gtk.ScrolledWindow()
    scrolledwindow_widget.set_policy(gtk.POLICY_NEVER, \
        gtk.POLICY_AUTOMATIC)
    scrolledwindow_widget.set_name('scrolledwindow_widget')
    scrolledwindow_widget.add(iconview_widget)
    widgets_table = gtk.Table(rows=1, columns=1)
    widgets_table.attach(scrolledwindow_widget, 0, 1, 0, 1, \
        xpadding=14, ypadding=14)
    dialog.vbox.pack_start(label, expand=False, fill=False, padding=4)
    dialog.vbox.pack_start(widgets_table)
    dialog.vbox.show_all()
    select_button = dialog.add_button('Select', gtk.RESPONSE_OK)
    select_button.set_size_request(262, 60)
    select_button.set_sensitive(False)            
    select_button.set_name('dialog_button')
    iconview_widget.connect('selection-changed', enable_select_button_cb, \
        select_button)
    cancel_button = dialog.add_button('Cancel', gtk.RESPONSE_REJECT)
    cancel_button.set_size_request(232, 60)
    cancel_button.set_name('dialog_button')
    dialog.action_area.set_layout(gtk.BUTTONBOX_SPREAD)
    dialog.action_area.set_homogeneous(True)
    return dialog, liststore, iconview_widget


def create_card_type_dialog_ui(selectors, front_to_back_id, both_ways_id, \
    three_sided_id, cloze_id, card_type_button, current_card_type, callback):
    """Creates CardType dialog UI."""

    button = create_radio_button(None, 'front_to_back_cardtype_button', \
        callback)
    selectors[front_to_back_id]['selector'] = button
    button = create_radio_button(button, 'both_ways_cardtype_button', callback)
    selectors[both_ways_id]['selector'] = button
    button = create_radio_button(button, 'three_sided_cardtype_button', \
        callback)
    selectors[three_sided_id]['selector'] = button
    button = create_radio_button(button, 'cloze_cardtype_button', callback)
    selectors[cloze_id]['selector'] = button
    dialog = gtk.Dialog()
    dialog.set_decorated(False)
    dialog.set_has_separator(False)
    pos_x, pos_y = card_type_button.window.get_origin()
    dialog.move(pos_x, pos_y)
    buttons_table = gtk.Table(rows=1, columns=4, homogeneous=True)
    buttons_table.set_col_spacings(16)
    index = 0
    for selector in selectors.values():
        widget = selector['selector']
        if current_card_type is selector['card_type']:
            widget.set_active(True)
        buttons_table.attach(widget, index, index + 1, 0, 1, \
            xoptions=gtk.EXPAND, xpadding=6)
        index += 1
    dialog.vbox.pack_start(buttons_table, expand=True, fill=False, \
        padding=12)
    buttons_table.show_all()
    dialog.run()


def create_content_dialog_ui(callback, content_button, toolbar_container, \
    current_card_type, front_to_back_id):
    """Creates ContentDialog UI."""

    text_content_button = create_button('text_content_button', callback, \
        width=72, height=72)
    image_content_button = create_button('image_content_button', callback, \
        width=72, height=72)
    sound_content_button = create_button('sound_content_button', callback, \
        width=72, height=72)
    dialog = gtk.Dialog()
    dialog.set_decorated(False)
    dialog.set_has_separator(False)
    pos_x, pos_y = content_button.window.get_origin()
    dialog.move(pos_x, pos_y + toolbar_container.get_size_request()[1]/5)
    state = current_card_type.id in (front_to_back_id)
    sound_content_button.set_sensitive(state)
    image_content_button.set_sensitive(state)
    buttons_table = gtk.Table(rows=1, columns=3, homogeneous=True)
    buttons_table.set_col_spacings(16)
    buttons_table.attach(text_content_button, 0, 1, 0, 1, \
        xoptions=gtk.EXPAND, xpadding=10)
    buttons_table.attach(sound_content_button, 1, 2, 0, 1, \
        xoptions=gtk.EXPAND, xpadding=10)
    buttons_table.attach(image_content_button, 2, 3, 0, 1, \
        xoptions=gtk.EXPAND, xpadding=10)
    buttons_table.show_all()
    dialog.vbox.pack_start(buttons_table, expand=True, fill=False, \
        padding=8)
    dialog.run()


def create_question_dialog(window, text):
    """Create QuestionDialog UI."""

    dialog = gtk.Dialog(parent=window, flags=gtk.DIALOG_MODAL|\
            gtk.DIALOG_DESTROY_WITH_PARENT|gtk.DIALOG_NO_SEPARATOR)
    dialog.set_decorated(False)
    button_yes = dialog.add_button('YES', gtk.RESPONSE_YES)
    button_yes.set_size_request(120, 80)
    button_yes.set_name('dialog_button')
    button_no = dialog.add_button('NO', gtk.RESPONSE_REJECT)
    button_no.set_size_request(120, 80)
    button_no.set_name('dialog_button')
    label = gtk.Label()
    label.set_name('dialog_label')
    label.set_text('\n' + text.replace('?', '?\n').replace(',', ',\n') + '\n')
    label.show()
    dialog.vbox.pack_start(label)
    dialog.vbox.set_spacing(2)
    response = dialog.run()
    dialog.destroy()
    if response == gtk.RESPONSE_YES:
        return False
    return True


def create_information_dialog(window, text):
    """Create InformationDialog UI."""
    
    dialog = gtk.Dialog(parent=window, flags=gtk.DIALOG_MODAL|\
        gtk.DIALOG_DESTROY_WITH_PARENT|gtk.DIALOG_NO_SEPARATOR)
    dialog.set_decorated(False)
    button_ok = dialog.add_button('OK', gtk.RESPONSE_OK)
    button_ok.set_size_request(120, 80)
    button_ok.set_name('dialog_button')
    label = gtk.Label()
    label.set_justify(gtk.JUSTIFY_CENTER)
    label.set_name('dialog_label')
    label.set_text('\n   ' + text.replace('.', '.   \n').replace( \
        ',', ',\n') + '\n')
    label.show()
    dialog.vbox.pack_start(label)
    dialog.action_area.set_layout(gtk.BUTTONBOX_SPREAD)
    dialog.run()
    dialog.destroy()


def create_button(name=None, callback=None, event='clicked', \
    width=80, height=80, label=None):
    """Creates gtkButton widget."""

    button = gtk.Button()
    button.set_size_request(width, height)
    if name is not None:
        button.set_name(name)
    if callback is not None:
        button.connect(event, callback)
    if label is not None:
        button.set_label(label)
    return button


def create_radio_button(group=None, name=None, callback=None, \
     event='released', width=72, height=72):
    """Creates gtkRadioButton widget."""

    button = gtk.RadioButton(group)
    button.set_size_request(width, height)
    if name is not None:
        button.set_name(name)
    if callback is not None:
        button.connect(event, callback)
    return button


def create_toolbar_container(name, show_tabs=False, width=82, height=480):
    """Creates toolbar container."""

    container = gtk.Notebook()
    container.set_show_tabs(show_tabs)
    container.set_size_request(width, height)
    container.set_name(name)
    return container


def create_tag_checkbox(name, active):
    """Create Tag item - GtkHBox with gtk.ToggleButton and gtk.Label."""

    hbox = gtk.HBox(homogeneous=False, spacing=10)
    button = gtk.ToggleButton()
    button.set_size_request(64, 64)
    button.set_active(active)
    button.set_name("tag_indicator")
    label = gtk.Label(name)
    label.set_name("black_label")
    hbox.pack_start(button, False)
    hbox.pack_start(label, False)
    hbox.show_all()
    return hbox
