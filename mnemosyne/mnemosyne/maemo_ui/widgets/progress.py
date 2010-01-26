
from mnemosyne.libmnemosyne.ui_components.dialogs import ProgressDialog


class MaemoProgressDlg(ProgressDialog):

    def __init__(self, component_manager):
        ProgressDialog.__init__(self, component_manager)

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_resizable(True)

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

        self.window.show()

	
    def set_range(self, minimum, maximum):
#        self.setRange(minimum, maximum)
        print "set_range ", minimum, maximum
        
    def set_text(self, text):
#        self.setLabelText(text)
        self.window.set_title(text)
        self.pbar.set_text(text)
        print "set_text ", text
        
    def set_value(self, value):
#        self.setValue(value)
        print "set_value ", value
	
import gtk, gobject

class ProgressBar:
    # Callback that toggles the text display within the progress
    # bar trough
    def toggle_show_text(self, widget, data=None):
        if widget.get_active():
            self.pbar.set_text("some text")
        else:
            self.pbar.set_text("")

    # Callback that toggles the activity mode of the progress
    # bar
    def toggle_activity_mode(self, widget, data=None):
        if widget.get_active():
            self.pbar.pulse()
        else:
            self.pbar.set_fraction(0.0)


    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_resizable(True)

        self.window.connect("destroy", self.destroy_progress)
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

        self.window.show()

	
