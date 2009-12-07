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
Hildon UI. Widgets for main.
"""

import gtk

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


