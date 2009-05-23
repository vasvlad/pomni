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
Hildon UI: Input mode classes.
"""

import gettext
import gtk
import gtk.glade

from os.path import splitext, basename

from mnemosyne.libmnemosyne.component_manager import database, config, \
        ui_controller_main, card_types

from pomni.hildon_ui import HildonBaseUi

_ = gettext.gettext


class HildonUiControllerInput(HildonBaseUi):
    """ Hildon Input controller. """

    def __init__(self):
        """ Initialization items of input window. """

        HildonBaseUi.__init__(self, signals=['add_card', 'change_card_type'])

        self.title = _("Mnemosyne") + " - " + \
            splitext(basename(config()["path"]))[0]
        self.card = ui_controller_main()


    def layout (self):
        """ Hides or shows neccessary widgets. It depends on card_type. """

        self.w_tree.get_widget("pronun_box").set_property(\
            'visible', self.card_type.id == '3')


    def set_card_type(self):
        """ Set card type when user select it in cardtypes combobox. """

        cardtypes = dict([(card_type.id, card_type) \
            for card_type in card_types()])
        selected_id = (int(self.w_tree.get_widget("cardtypes").get_active())\
            + 1).__str__()
        self.card_type = cardtypes.get(selected_id)


    def change_card_type_cb(self, widget):
        """ Changes cardtype when user choose it from listbox. """

        self.set_card_type()
        self.layout()


    def start(self, w_tree):
        """ Start input window. """
        
        self.w_tree = w_tree
        self.switcher.set_current_page(self.input)

        # Fill Categories list
        # categories = { id:category, ...}
        categories = dict([(i, name) for (i, name) in \
            enumerate(database().category_names())])
        categories_widget = w_tree.get_widget("categories")
        categories_liststore = gtk.ListStore(str)
        for category in sorted(categories.values()):
            categories_liststore.append([category])
        categories_widget.set_model(categories_liststore)
        categories_widget.set_text_column(0)
        if categories.values():
            categories_widget.get_child().set_text(\
                sorted(categories.values())[0])
        
        # Fill Card-types list
        # cardtypes = { id:card_type_object, ...}
        cardtypes = dict([(card_type.id, card_type) \
            for card_type in card_types()])
        cardtypes_widget = w_tree.get_widget("cardtypes")
        cardtypes_liststore = gtk.ListStore(str)
        for key in sorted(cardtypes.keys()):
            cardtypes_liststore.append([cardtypes.get(key).name])
        cardtypes_widget.set_model(cardtypes_liststore)
        cardtypes_widget.set_text_column(0)
        if cardtypes:
            cardtypes_widget.get_child().set_text(\
                cardtypes.get(sorted(cardtypes.keys())[0]).name)
        self.card_type = cardtypes.get(sorted(cardtypes.keys())[0])
        self.layout()

        HildonBaseUi.start(self, w_tree)


    def add_card_cb(self, widget):
        """ Add card to database. """

        try:
            fact_data = self.get_widgets_data()
        except ValueError:
            return # Let the user try again to fill out the missing data.

        # Create new card
        #self.card = ui_controller_main()
        self.card.create_new_cards(fact_data, self.card_type, 0, [\
            self.w_tree.get_widget("categories").get_child().get_text()], True)
        database().save(config()['path'])
        self.clear_widgets()


    def get_widgets_data(self, check_for_required=True):
        """ Get data from widgets. """

        fact = {}
        question_widget = self.w_tree.get_widget("question_box_text")
        answer_widget = self.w_tree.get_widget("answer_box_text")
        pronunciation_widget = self.w_tree.get_widget("pronun_box_text")
        if self.card_type.id == '3':
            widgets = [('f', question_widget), ('t', answer_widget), \
                ('p', pronunciation_widget)]
        else:
            widgets = [('q', question_widget), ('a', answer_widget)]
        for fact_key, widget in widgets:
            start, end = widget.get_buffer().get_bounds()
            fact[fact_key] = widget.get_buffer().get_text(start, end)

        if check_for_required:
            for required in self.card_type.required_fields():
                if not fact[required]:
                    raise ValueError
        return fact


    def clear_widgets(self):
        """ Clear data in widgets. """

        self.w_tree.get_widget("question_box_text").get_buffer().set_text("")
        self.w_tree.get_widget("answer_box_text").get_buffer().set_text("")
        self.w_tree.get_widget("pronun_box_text").get_buffer().set_text("")




class EternalControllerInput(HildonUiControllerInput):
    """ Eternal Input mode controller """
    


class RainbowControllerInput(HildonUiControllerInput):
    """ Rainbow Input mode controller """



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
