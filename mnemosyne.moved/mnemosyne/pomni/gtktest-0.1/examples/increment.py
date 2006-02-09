#!/usr/bin/env python
import gtk

class ExampleApp(object):

    label = None
    num = 0

    def __init__(self):
        self.win = gtk.Window()
        self.win.set_border_width(12)
        self.win.connect('delete-event', self.quit)

        self.button = gtk.Button("Increment")
        self.button.connect('clicked', self.btnclick)
        self.label = gtk.Label("#")

        self.box = gtk.HBox()
        self.box.set_spacing(12)
        self.box.add(self.button)
        self.box.add(self.label)

        self.win.add(self.box)
        self.win.show_all()

    def run(self):
        gtk.main()

    def quit(self, *ignored):
        gtk.main_quit()
        return False

    def btnclick(self, button):
        self.num += 1
        self.label.set_text(str(self.num))


def main():
    global app # hook for tests
    app = ExampleApp()
    app.run()

if __name__ == '__main__':
    main()
