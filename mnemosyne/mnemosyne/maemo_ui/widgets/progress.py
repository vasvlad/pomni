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
Hildon UI. Widget for progressbar window.
"""

from mnemosyne.libmnemosyne.ui_components.dialogs import ProgressDialog
import gtk

class MaemoProgressDlg(ProgressDialog):
    """ Class for ProgressDlg in libmnemosyne. It using in factory"""

    def __init__(self, component_manager):
        ProgressDialog.__init__(self, component_manager)
        
        self.window = None
        self.fraction = 0.0
        try:
            import hildon
            self.pbar = hildon.hildon_banner_show_progress(\
                        self.main_widget().window, None, "")
            self.pbar.show()
        except ImportError:

            self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)

            self.window.set_title("ProgressBar")
            self.window.set_border_width(0)

            vbox = gtk.VBox(False, 5)
            vbox.set_border_width(10)
            self.window.add(vbox)
            vbox.show()
     
            # Create a centering alignment object
            align = gtk.Alignment(0.5, 0.5, 0, 0)
            vbox.pack_start(align, False, False, 5)
            align.show()

            # Create the ProgressBar
            self.pbar = gtk.ProgressBar()

            align.add(self.pbar)
            self.pbar.show()

            separator = gtk.HSeparator()
            vbox.pack_start(separator, False, False, 0)
            separator.show()

            # rows, columns, homogeneous
            table = gtk.Table(2, 2, False)
            vbox.pack_start(table, False, True, 0)
            table.show()


	
    def set_range(self, minimum, maximum):
        """Calculate fraction for progressbar """

        self.fraction = float(1.0/(maximum-minimum))
        if self.window:
            self.window.show()
       
    def set_text(self, text):
        """Set title on progress bar """

        self.pbar.set_text(text)
        
    def set_value(self, value):
        """Set new value for progess bar """ 

        self.pbar.set_fraction(value * self.fraction)
        if value * self.fraction > 0.999 :
            if self.window:
                self.window.destroy()
            else:
                self.pbar.destroy()
 
        #Pending gtk
        while gtk.events_pending():
            gtk.main_iteration(False)

