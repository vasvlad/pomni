#!/usr/bin/env python2.5
# vim:ts=4:sw=4:expandtab:ai
# Test for pomni
""" Version 3 For test only"""

import gtk
import hildon

#Global varios
FULLSCREEN = False



def on_window_state_change(widget, event):
    """Changed global various FULLSCREEN""" 
    global FULLSCREEN

    if event.new_window_state & gtk.gdk.WINDOW_STATE_FULLSCREEN:
        FULLSCREEN = True
    else:
        FULLSCREEN = False


def on_key_press(widget, event):
    """Changed window state between FULLSCREEN and non FULLSCREEN"""

    if event.keyval == gtk.keysyms.F6:
        if FULLSCREEN:
            widget.unfullscreen()
        else:
            widget.fullscreen()

def show_message(widget, message):
    """ Show some message """
    
    hildon.hildon_banner_show_information(widget, None, message)

def green_message(widget, event):
    """ Preparing message about green button """
    
    show_message(widget, "Pressed Green button")

def red_message(widget, event):
    """ Preparing message about red button """
    
    show_message(widget, "Pressed Red button")

def gray_message(widget, event):
    """ Preparing message about gray button """
    
    show_message(widget, "Pressed Gray button")
    
    
def new_button(widget, function, image_file):
    """ Add image and function to eventbox """

    image = gtk.Image()
    image.set_from_file(image_file)
    widget.add(image)
    widget.connect("button-press-event", function)
    image.show()
    widget.show()
    
def main():
    """ Main part of program """
    
    window = hildon.Window()
    window.set_title("Pomni")
    window.connect("destroy", gtk.main_quit)
    window.connect("key-press-event", on_key_press)
    window.connect("window-state-event", on_window_state_change)

    #Simple label
    label = gtk.Label("Press button 'Fullscreen' for \
    testing in fullscreen mode")
    label.show()
    
    #Area for editing text
    frame = gtk.Frame("Area for text")
    scrwnd = gtk.ScrolledWindow()
    scrwnd.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
    textview = gtk.TextView()
    textbuffer = textview.get_buffer()
    textbuffer.set_text("Edit me, please")
    scrwnd.add(textview)
    scrwnd.show()
    textview.show()
    frame.add(scrwnd)
    frame.show()
    
    hbox = gtk.HBox(False, 0)
    
    #Red button
    evbox_red = gtk.EventBox()
    new_button(evbox_red, red_message, "red.png")
    hbox.pack_start(evbox_red, True, False, 0)
    #Green button
    evbox_green = gtk.EventBox()
    new_button(evbox_green, green_message, "refresh.png")
    hbox.pack_start(evbox_green, True, False, 0)
    #Gray button
    evbox = gtk.EventBox()
    new_button(evbox, gray_message, "about.png")
    hbox.pack_start(evbox, True, False, 0)

    hbox.show()

    #Packing to window
    vbox = gtk.VBox(False, 0)
    vbox.pack_start(label, True, True, 5)
    vbox.pack_start(frame, True, True, 5)
    vbox.pack_start(hbox, True, True, 5)
    vbox.show()
    window.add(vbox)

    window.show()
    gtk.main()

if __name__ == '__main__':
    main()

