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

        self.model = model
        model.register(self)

    def update(self, model):
        """ This method is part of Observer pattern
            it's called by observable(Model in our case) to notify
            about its change
        """
        pass

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
        c = ui_controller_main()
        #Default type for Comandline Interface is "Front-to-back only"
        print "Select Card Type:"
        for card_type in card_types():
            print card_type.id,".",card_type.name

        # Default category for Comandline Interface is 'category1'
        category = 'category1'
        while once_again == "y":
            face_side = raw_input("Enter the face side: ")
            back_side = raw_input("Enter the back side: ")
            c.create_new_cards({'q': face_side, 'a': back_side}, card_type, 0, category)
            once_again = raw_input("Do you want to add a new record? y/n ")
	    
        database().save(config()['path'])
       
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
