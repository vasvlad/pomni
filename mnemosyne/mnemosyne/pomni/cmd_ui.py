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
import locale
import codecs

from mnemosyne.libmnemosyne.component_manager import database, scheduler, \
        ui_controller_review, config, ui_controller_main, card_types
from mnemosyne.libmnemosyne.ui_controller_review import UiControllerReview

class CmdUiControllerException(Exception):
    """ This module's exception type """
    pass

_ = gettext.gettext

class CommandlineUI(cmd.Cmd):
    """ Commandline UI. Upper-level class """

    def __init__(self):

        cmd.Cmd.__init__(self)
        self.prompt = '====== Main =======\nPomni: '
        ui_controller_main().widget = self

    def information_box(self, message, ok_string):
        """ Widget method. DefaultMainController.create_new_cards calls it """
        print message

    def question_box(self, question, option0, option1, option2):
        """ Widget method. DefaultMainController.create_new_cards calls it """
        print question
        print "0", option0
        print "1", option1
        print "2", option2
        answer = raw_input(_("Enter number of answer for select it "))

        return answer

    def start(self, mode):
        """ UI entry point. Called by controller  """
        if not mode or mode == 'main':
            self.cmdloop()
        else:
            self.onecmd(mode)

    def do_quit(self, line):
        """ Quit the program """ 
        return True

    def do_review(self, line):
        """ Review mode """
        ui_controller_review().start()

    def do_input(self, line):
        """ Input mode """
        print("=== Input mode ===")

        card = ui_controller_main()
        
        card_type_by_id = dict([(card_type.id, card_type) \
            for card_type in card_types()])
        
        category_names_by_id = dict([(i, name) for (i, name) in \
            enumerate(database().category_names())])
        
        while True:
            # Select Card Type by user:
            print "Select Card Type:"
            print '\n'.join(["%s %s" % (type_id, card_type_by_id[type_id].name) \
                for type_id in sorted(card_type_by_id.keys())])
            while True:
                inp = \
                raw_input(_("Enter number of Card Type or 'q' to quit ... "))
                if inp in ("q", "Q"):
                    return
                if inp in card_type_by_id:
                    card_type = card_type_by_id[inp]
                    break
                print(_("Input error, try again"))

            # Select the exist or Add the new Category
            print '\n'.join(["%s %s" % (cat_id, category_names_by_id[cat_id]) \
                for cat_id in sorted(category_names_by_id.keys())])
            inp = raw_input(_("Enter number of Category or "\
                "enter new category or 'q' to quit ... "))
            if inp in ("q", "Q"):
                return
            category_name = inp
            if inp in category_names_by_id:
                category_name = category_names_by_id[inp]

            # Enter all fields for the current type
            fact = {}
            for key, name in card_type.fields:
                print _("Enter field"), name
                inp = raw_input()
                if inp:
                    fact[key] = inp

            # Check necesary fields and create new card
            for required in card_type.required_fields():
                if required not in fact:
                    print(_("Error.This card is not saved in a database !!!"))
                    print(_("You didn't enter all necesary field(s) !!!"))
                    break
            else:
                # Create new card
                card.create_new_cards(fact, card_type, 0, [category_name])
                database().save(config()['path'])

            if raw_input(_("Do you want to add a new record? y/n ")) != "y":
                break
	    
       
    def do_conf(self, line):
        """ Configuration mode """

        def get_param(conf, param):
            """ Get current param value """
            if param not in conf:
                print param, "is not exist. Try another!"
                return ''
            return conf[param]

        cfg = config()  # create instance
        cfg.load()      # load parameters from configuration file
        print "=== Config mode ==="
        print "Type 'help' to view config commands or 'quit' to quit."

        help_promt = \
            "\thelp - This information\n\tquit - Quit from Config mode"\
            "\n\tshow - Show current configuration"\
            "\n\tset - Set new param value"\
            "\n\tget - Get current param value"\
            "\n\tsave - Save current configuration"

        user_cmd = 'nocmd'
        while user_cmd != 'quit':
            user_cmd = raw_input("conf: ")
            if user_cmd == 'help':
                print help_promt
            elif user_cmd == 'show':
                print '\n'.join(["%s:%s" % item for item in cfg.items()])
            elif user_cmd == 'set':
                param = raw_input("Enter param name: ")
                value = raw_input("Enter new value: ")
                cfg[param] = value
            elif user_cmd == 'get':
                param = raw_input("Enter param name: ")
                print get_param(cfg, param)
            elif user_cmd == 'save':
                cfg.save()
            elif user_cmd != 'quit':
                print 'Unknown command. Type another!'


class CmdUiControllerReview(UiControllerReview):
    """ Commandline UI controller. Review mode """
    
    def __init__(self):
        
        UiControllerReview.__init__(self, name="Command line UI Controller")
        self.title = _("Mnemosyne") + " - " + \
            os.path.basename(config()["path"])[:-4]
        self.grade = 0
        self.learn_ahead = False

    def update_dialog(self):
        """ This is part of UiControllerReview API """
        pass

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

    def new_question(self):
        """ Print new question """

        if database().card_count() == 0:
            raise CmdUiControllerException(_("Database is empty"))
        else:
            self.card = scheduler().get_new_question(self.learn_ahead)
            if self.card != None:
                print _("Question:"), self.card.question()
            else:
                value = raw_input(_("Learn ahead of schedule" + "? (y/N)"))
                if value in ("y", "Y"):
                    print("\n")
                    self.learn_ahead = True
                    self.new_question()
                else:
                    raise CmdUiControllerException(_("Finished"))

    def show_answer(self):
        """ Print answer or quit  """

        value = raw_input(_("Press enter to see the answer or 'q' to quit ..."))
        if value in ("q", "Q"):
            raise CmdUiControllerException(_("Exited"))

        # get current encoding
        encoding = None
        preferred_enc = locale.getpreferredencoding()
        if preferred_enc in locale.locale_encoding_alias:
            encoding = locale.locale_encoding_alias[preferred_enc]

        answer = self.card.answer()
        if encoding:
            answer = codecs.encode(answer, encoding)
        print(_("Answer: %s" % answer))

    def grade_answer(self):
        """ Get grade from the user and process it """

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
