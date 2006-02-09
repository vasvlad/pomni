#!/usr/bin/env python

"""An example for GtkTestCase."""

import unittest
import gtktest
import gtk.gdk
from gtktest import GtkTestCase, mainloop_handler, gtkinfo

import increment # app being tested


class TestExample(GtkTestCase):

    #@mainloop_handler(increment.main)
    def test_simple(self):
        assert increment.app
    test_simple = mainloop_handler(increment.main)(test_simple)

    def test_complex(self):
        app = increment.ExampleApp()
        assert app.win.get_border_width() == 12
        assert app.box.get_spacing() == 12
        assert app.label.get_parent() is app.box
        assert app.button.get_parent() is app.box
        assert app.label.get_label() == '#'
        for x in range(1, 10):
            app.button.clicked()
            assert app.num == x
            assert app.label.get_label() == str(x)

    def test_quit(self):
        app = increment.ExampleApp()
        assert gtkinfo.level == 0
        app.win.emit('delete-event', gtk.gdk.Event(gtk.gdk.DELETE))
        assert gtkinfo.level == -1


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestExample))
    return suite


if __name__ == '__main__':
    unittest.main()
