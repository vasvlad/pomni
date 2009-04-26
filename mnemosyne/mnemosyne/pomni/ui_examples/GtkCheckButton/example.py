#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade


class TestApplication:
    def __init__(self):
        self.gladefile = "checkbox.glade"
        self.w_tree = gtk.glade.XML(self.gladefile)
        self.window = self.w_tree.get_widget("window")
        self.window.connect("destroy", gtk.main_quit)
        gtk.rc_parse("rcfile")
        self.window.show()
        

if __name__ == "__main__":
    app = TestApplication()
    gtk.main()

