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
Command-line UI
"""

import os
import gettext
import cmd
from os.path import basename

from mnemosyne.libmnemosyne.component_manager import database, scheduler, \
        ui_controller_review, config, ui_controller_main, card_types
from mnemosyne.libmnemosyne.ui_controller_review import UiControllerReview
from mnemosyne.libmnemosyne.ui_controllers_review.SM2_controller \
    import SM2Controller

class CmdUiControllerException(Exception): pass

_ = gettext.gettext

class CommandlineUI(cmd.Cmd):
    """ Commandline UI. Upper-level class """

    def __init__(self, model):
        cmd.Cmd.__init__(self)
        self.prompt = '====== Main =======\nPomni: '
        ui_controller_main().widget = self
        self.model = model
        model.register(self)

    def update(self, model):
        """ This method is part of Observer pattern
            it's called by observable(Model in our case) to notify
            about its change
        """
        pass

    def information_box(self, message, OK_string):
        print message

    def question_box(self, question, option0, option1, option2):
        print question
        print "0", option0
        print "1", option1
        print "2", option2
        answer = raw_input(_("Enter number of answer for select it "))

        return answer

    def start(self, mode):
        if mode:
            self.onecmd(mode)
        else:
            self.cmdloop()

    def do_quit(self, line):
        """ Quit the program """ 
        return True

    def do_review(self, line):
        """ Review mode """
        ui_controller_review().start()

    def do_input(self, line):
        """ Input mode """
        print("=== Input mode ===")

        once_again = "y"
        card = ui_controller_main()
        while once_again == "y":
            # Select Card Type by user:
            print "Select Card Type:"
            card_type_by_id = {}
            for card_type in card_types():
                print card_type.id, card_type.name
                card_type_by_id[card_type.id] = card_type

            while True:
                card_type_id = \
                raw_input(_("Enter number of Card Type or 'q' to quit ... "))
                if card_type_id in ("q", "Q"):
                    return
                try:
                    card_type = card_type_by_id[card_type_id]
                except KeyError:
                    print(_("Input error, try again"))
                    continue
                break

            # Select the exist or Add the new Categore  
            i = 0
            category_names_by_id = {}
            for name in database().category_names():
                print i,name
                category_names_by_id[str(i)] = name 
                i=i+1
 
            while True:
                category_name_id = \
                raw_input(_("Enter number of Category or enter new category or 'q' to quit ... "))
                if category_name_id in ("q", "Q"):
                    return
                try:
                     category_name = category_names_by_id[category_name_id]
                except KeyError:
                    category_name = category_name_id
                break


            # Enter all fields for the current type
            fact = {}
            problem_field = False
            for fact_key, fact_key_name in card_type.fields:
                print _("Enter field"), fact_key_name
                text = raw_input()
                if text:
                    fact[fact_key] = text
            # Check necesary fields and create new card
            for required in card_type.required_fields():
                if not required in fact.keys():
                    print(_("Error.This card is not saved in a database !!!"))
                    print(_("You didn't enter all necesary field(s) !!!"))
                    problem_field = True
            # Create new card
            if not problem_field :
                card.create_new_cards(fact, card_type, 0, [category_name])
                database().save(config()['path'])

            once_again = raw_input(_("Do you want to add a new record? y/n "))
	    
       
    def do_conf(self, line):
        """ Configuration mode """
        print "Configuration mode. Not implemented yet"

class CmdUiControllerReview(UiControllerReview):
    """ Commandline UI controller. Review mode """
    
    def __init__(self):
        # FIXME - should call parent's __init__, not grandparent's
        UiControllerReview.__init__(self, name="Command line UI Controller")
        self.title = _("Mnemosyne") + " - " + basename(config()["path"])[:-4]
        self.grade = 0

    def start(self):
        """ UI Entry point """
        print("\nReview mode. Category: %s\n" % self.title)
        while True:
            try:
                self.new_question()
                self.show_answer()
                self.grade_answer()
            except CmdUiControllerException, exobj:
                print(exobj)
                break

    def new_question(self, learn_ahead=False):
        if database().card_count() == 0:
            raise CmdUiControllerException(_("Database is empty"))
        else:
            self.card = scheduler().get_new_question(learn_ahead)
            if self.card != None:
                print _("Question:"), self.card.question()
            else:
                value = raw_input(_("Learn ahead of schedule" + "? (y/N)"))
                if value in ("y", "Y"):
                    print("\n")
                    self.new_question(learn_ahead=True)
                else:
                    raise CmdUiControllerException(_("Finished"))

    def show_answer(self):
        value = raw_input(_("Press enter to see the answer or 'q' to quit ..."))
        if value in ("q", "Q"):
            raise CmdUiControllerException(_("Exited"))
        print(_("Answer: %s" % self.card.answer()))

    def grade_answer(self):
        while True:
            try:
                grade = raw_input(_("Grade your answer:"))
            except SyntaxError:
                print(_("Input error, try again"))
                continue
            if not grade.isdigit():
                print(_("Input error: Grade has to be a number from 0 to 5"))
                continue
            grade = int(grade)
            if not 0 <= grade <= 5:
                print(_("Input error: Grade has to be a number from 0 to 5"))
                continue

            scheduler().process_answer(self.card, grade)
            print("\n")
            break


class CmdReviewWdgt:
    pass

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