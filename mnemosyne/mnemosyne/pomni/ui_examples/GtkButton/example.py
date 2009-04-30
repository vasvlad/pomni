#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade


class Application:
    def __init__(self):
        self.gladefile = "button.glade"
        self.w_tree = gtk.glade.XML(self.gladefile)
        self.window = self.w_tree.get_widget("window1")
        self.window.connect("destroy", gtk.main_quit)
        gtk.rc_parse("rcfile")
        self.window.show()
        

if __name__ == "__main__":
    app = Application()
    gtk.main()

