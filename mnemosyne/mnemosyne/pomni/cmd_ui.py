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

class CommandlineUI:
    """ Commandline UI """

    def __init__(self, model):
        self.model = model
        model.register(self)

    def main_mode(self):
        """ Main mode - examine cards """

        print("=== Main mode ===")
        model = self.model
        for name, card in model.scheduled():
            print("\nFace: %s" % name)
            raw_input("Press enter to see the other side ...")
            print("Back: %s" % card["back"])
            while True:
                try:
                    mark = raw_input("Enter the mark:")
                except SyntaxError:
                    print("Input error, try again")
                    continue

                try:
                    model.update_mark(name, mark)
                except model.ModelException, exobj:
                    print(str(exobj) + ", try again")
                else:
                    break

        print "=== Session statistics ==="
        for name, card in model.scheduled():
            print(name, card)

    def update(self, model):
        """ This method is part of Observer pattern
        it's called by observable(Model in our case) to notify
        about its change
        """

        pass

    def fill_mode(self):
        """ Fill mode - fill both record of card """

        print("=== Fill mode ===")
        model = self.model
        backend = model.backend
        once_again = "y"
        while once_again == "y":
            face_side = raw_input("Enter the face side: ")
            back_side = raw_input("Enter the back side: ")
            backend.add_field(face_side, back_side) 
            once_again = raw_input("Do you want to add a new record? y/n ")

        print "=== Session statistics ==="
        for name, card in model.scheduled():
            print(name, card)

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
