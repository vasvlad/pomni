#! /usr/bin/python
# vim: sw=4 ts=4 expandtab ai

import hildon
import gtk

class App():
    def __init__(self):
    	self.fullscreen_mode = True
	self.program_mode = "study"
        self.window = hildon.Window()
	self.window.set_title("Pomni")
	self.window.connect("delete_event", self.delete_event)
	self.window.connect("key-press-event", self.on_key_press)
	self.window.connect("window-state-event", self.on_window_state_change)
	
	#create widgets
	self.button_choose = self.create_button("choose.png")
	self.button_edit = self.create_button("edit.png")
	self.button_conf = self.create_button("conf.png")
	self.button_question = self.create_button("question.png")
	self.button_1 = self.create_button("face1.png")
	self.button_2 = self.create_button("face2.png")
	self.button_3 = self.create_button("face3.png")
	self.button_4 = self.create_button("face4.png")
	self.button_5 = self.create_button("face5.png")
	self.button_quit = self.create_button("quit.png")
	self.button_quit.connect("button-press-event", self.delete_event)
	self.button_pomni = self.create_button(None, "Pomni")
	t1, self.textbox_question = self.create_textbox(" Question ", "How do you assess it?")
	self.textbox_question.set_editable(False)
	t2, self.textbox_answer = self.create_textbox(" Answer ", "0 or 2 or 3 or 4 or 5")

	self.table = gtk.Table(24, 40, True)
        self.table.set_border_width(5)
        self.window.add(self.table)

	#add widgets to the Table
        self.table.attach(self.button_1, 2, 5, 19, 24)
        self.table.attach(self.button_2, 9, 12, 19, 24)
        self.table.attach(self.button_3, 16, 19, 19, 24)
        self.table.attach(self.button_4, 23, 26, 19, 24)
        self.table.attach(self.button_5, 29, 33, 19, 24)
        self.table.attach(self.button_quit, 0, 2, 0, 2)
        self.table.attach(self.button_pomni, 0, 40, 0, 2)
        self.table.attach(t1, 1, 34, 3, 10)
        self.table.attach(t2, 1, 34, 11, 18)
        self.table.attach(self.button_choose, 35, 40, 3, 7)
        self.table.attach(self.button_edit, 35, 40, 8, 12)
        self.table.attach(self.button_conf, 35, 40, 13, 16)
        self.table.attach(self.button_question, 35, 40, 19, 24)
	self.table.show()
	self.window.fullscreen()
	self.window.show()


    def create_button(self, image_file_name, caption=''):
        """ creates single button """
    	eventBox = gtk.EventBox()
	if caption == '':
	    image = gtk.Image()
	    image.set_from_file(image_file_name)
	    eventBox.add(image)
	    image.show()
	else:
	    label = gtk.Label(caption)
	    eventBox.add(label)
	    label.show()
	eventBox.show()
	return eventBox


    def create_textbox(self, caption = '', start_text = ''):
	""" cteate textbox"""
    	scrolled_window = gtk.ScrolledWindow()
	scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        frame = gtk.Frame(caption)
	textbox = gtk.TextView()
	textbox.get_buffer().set_text(start_text)
	textbox.set_cursor_visible(False)
	textbox.set_justification(gtk.JUSTIFY_CENTER)
	scrolled_window.add(textbox)
	frame.add(scrolled_window)
	textbox.show()
	frame.show()
	scrolled_window.show()
	return (frame, textbox)


    def main(self):
        gtk.main()


    def on_key_press(self, widget, event):
        if event.keyval == gtk.keysyms.F6:
            if self.fullscreen_mode:
                widget.unfullscreen()
            else:
                widget.fullscreen()


    def on_window_state_change(self, widget, event):
        if event.new_window_state & gtk.gdk.WINDOW_STATE_FULLSCREEN:
            self.fullscreen_mode  = True
        else:
            self.fullscreen_mode = False


    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
	return False



if __name__ == "__main__":
    app = App()
    app.main()

