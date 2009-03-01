#!/usr/bin/python -tt7
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
Hildon UI
"""

import os
import gettext
import gtk
import gtk.glade
import gtkhtml2

from os.path import splitext, basename

from mnemosyne.libmnemosyne.component_manager import database, scheduler, \
        config, ui_controller_main, card_types
from mnemosyne.libmnemosyne.ui_controller_review import UiControllerReview

_ = gettext.gettext


class HildonUiControllerException(Exception):
    """ Exception hook """

    def __init__(self, w_tree, exception):
        """ Show Warning Window """

        w_tree.signal_autoconnect({"close": self.close_cb})
        
        # Show warning text
        w_tree.get_widget("label_warning").set_text(exception)
        self.warning_window = w_tree.get_widget("warningwindow")
        self.warning_window.show()

        Exception.__init__(self)

    def close_cb(self, widget, event):
        """ Close Warning Window """
        self.warning_window.hide()


class HildonBaseUi():
    """ Base Hildon UI functionality """

    # page's indexes in switcher
    main_menu, review, input, config = range(4)

    def __init__(self, signals):

        self.signals = ["to_main_menu"]

        if signals:
            self.signals.extend(signals)

        self.w_tree = None

    def __getattr__(self, name):
        """ Lazy get widget as an attribute """

        widget = self.w_tree.get_widget(name)
        if widget:
            return widget
        raise AttributeError()

    def start(self, w_tree):
        """ Init w_tree, connect callbacks to signals """

        self.w_tree = w_tree

        # connect signals to methods
        w_tree.signal_autoconnect(dict([(sig, getattr(self, sig + "_cb")) \
            for sig in self.signals]))

    def to_main_menu_cb(self, widget, event):
        """ Return to main menu """

        self.switcher.set_current_page(self.main_menu)


class HildonUiControllerReview(HildonBaseUi, UiControllerReview):
    """ Hildon Review controller """

    def __init__(self):
        """ Initialization items of review window """

        HildonBaseUi.__init__(self, signals=["get_answer", \
            "grade", "delete_card"])
        UiControllerReview.__init__(self)

        self.title = _("Mnemosyne") + " - " + \
            splitext(basename(config()["path"]))[0]

        self.grade = 0
        self.card = None


    def start(self, w_tree):
        """ Start new review window """

        HildonBaseUi.start(self, w_tree)


        # switch to Page review
        # switcher - window with tabs. Each tab is for
        # different mode (main_menu, review, conf, input, etc)
        self.switcher.set_current_page(self.review)

        # Begin the review window from a new question
        self.new_question()

    # UiControllerReview API


    def update_dialog(self, redraw_all):
        """ This is part of UiControllerReview API """

        self.new_question()

    def new_question(self, learn_ahead=False):
        """ Create new question """

        if not database().card_count():
            raise HildonUiControllerException(self.w_tree, \
                _("Database is empty"))

        self.card = scheduler().get_new_question(learn_ahead)

        if self.card:
            document = getattr(self,'question_text').document
            view = getattr(self,'question_text')
            document.clear()
            document.open_stream('text/html')
            # Adapting for html
            question_text = self.card.question()

            #FIXME Need check for space before <html>
            if question_text.startswith('<html>'):
                font_size = view.get_style().font_desc.get_size()/1024
                font_size_from_config = config()['font_size']
                question_text = question_text.replace('*{font-size:30px;}',
                 '*{font-size:%spx;}' % font_size_from_config)
            else:
                # FIXME
                print "Not a html!!!!!!!!!"
            document.write_stream(question_text)
            document.close_stream()


        else:
            # FIXME value = raw_input(_("Learn ahead of schedule" + "? (y/N)"))
            self.new_question(True)
            #self.question.set_text(card.question())

        for widget in [getattr(self, "grade%i" % num) for num in range(6)]:
            widget.set_sensitive(False)
        self.get_answer.set_sensitive(True)
#        self.card = card

    def show_answer(self):
        """ Show answer in review window """

        for widget in [getattr(self, "grade%i" % num) for num in range(6)]:
            widget.set_sensitive(True)
        self.get_answer.set_sensitive(False)

        view = getattr(self,'answer_text')
        answer_text = self.card.answer()
        document = getattr(self,'answer_text').document
        document.clear()
        document.open_stream('text/html')
        # Adapting for html
        #FIXME Need check for space before <html>
        if answer_text.startswith('<html>'):
            font_size = view.get_style().font_desc.get_size()/1024
            font_size_from_config = config()['font_size']
            answer_text = answer_text.replace('*{font-size:30px;}',
                             '*{font-size:%spx;}' % font_size_from_config)
            #answer_text = answer_text.replace('<head>', 
            #'<head> <style>*{font-size:%spx;}</style>' % font_size)
        else:
            # FIXME
            print "Not a html!!!!!!!!!"

        document.write_stream(answer_text)
        document.close_stream()


    def grade_answer(self, grade):
        """ Grade the answer """

        scheduler().process_answer(self.card, grade)
        self.new_question()

    # Glade callbacks

    def get_answer_cb(self, widget, event):
        """ Hook for showing a right answer """

        self.show_answer()

    @staticmethod
    def delete_card_cb(widget, event):
        """ Hook for showing a right answer """

        # Create new card
        main = ui_controller_main()
        main.delete_current_fact()

    def grade_cb(self, widget, event):
        """ Call grade of answer """

        self.grade_answer(int(widget.name[-1]))

    def clear(self):
        """ Unknown """

        self.card = None


class HildonUiControllerInput(HildonBaseUi):
    """ Hildon Input controller """

    def __init__(self):
        """ Initialization items of input window """

        HildonBaseUi.__init__(self, signals=['add_card', 'add_card2'])

        self.title = _("Mnemosyne") + " - " + \
            splitext(basename(config()["path"]))[0]
        self.fields_container = None
        self.liststore = None
        self.card_type = None
        self.w_tree = None
        self.edit_boxes = {}

    def create_entries (self):
        ''' Create widget inclusive varios entries '''

        fields_container = gtk.VBox()
        fields_container.set_name('fields_container')
        fields_container.show()
        for fact_key, fact_key_name in self.card_type.fields:
            # Top Alignment
            aligment = gtk.Alignment()
            aligment.set_property("height-request", 100)
            fields_container.pack_start(aligment, True, True, 0)
            # Label of field
            labelbox = gtk.HBox()
            left_aligment_of_label = gtk.Alignment()
            left_aligment_of_label.set_property("width-request", 10)
            left_aligment_of_label.show()
            name_field = gtk.Label(fact_key_name)
            labelbox.pack_start(left_aligment_of_label, False, False, 0)
            labelbox.pack_start(name_field, False, False, 0)
            labelbox.pack_start(gtk.Alignment(), True, True, 0)
            name_field.show()
            labelbox.show()
            fields_container.pack_start(labelbox, True, True, 0)
            # Entry
            framebox = gtk.HBox()
            #Left Alignment
            left_aligment_of_frame = gtk.Alignment()
            left_aligment_of_frame.set_property("width-request", 10)
            left_aligment_of_frame.show()
            framebox.pack_start(left_aligment_of_frame, False, False, 0)
            #TextView itself
            surface = gtk.Notebook()
            surface.set_property('show_tabs', False)
            surface.set_name('question_frame')
            entry_field = gtk.TextView()
            entry_field.set_property("height-request", 50)
            entry_field.set_name(fact_key_name)
            entry_field.show()
            self.edit_boxes[entry_field] = fact_key
            surface.append_page(entry_field)
            framebox.pack_start(surface, True, True, 0)
            surface.show()
            #Right Alignment
            right_aligment_of_frame = gtk.Alignment()
            right_aligment_of_frame.set_property("width-request", 10)
            framebox.pack_start(right_aligment_of_frame, False, False, 0)
            right_aligment_of_frame.show()
            framebox.show()

            fields_container.pack_start(framebox, True, True, 0)

        return fields_container

    def start(self, w_tree):
        """ Start input window """
        
        self.w_tree = w_tree
        card_type_by_id = dict([(card_type.id, card_type) \
            for card_type in card_types()])

        #FIX ME for all types of card 
        #Now default card type 1 (Front-to-back only) 
        self.card_type = card_type_by_id.get('1')

        #Prepare fields_container
        parent_fields_container = w_tree.get_widget('fields_container_parent')
        self.fields_container = self.create_entries()
        parent_fields_container.pack_start(self.fields_container, True, True, 0)

        category_names_by_id = dict([(i, name) for (i, name) in \
            enumerate(database().category_names())])

        HildonBaseUi.start(self, w_tree)

        # switch to Page Input
        self.switcher.set_current_page(self.input)

        categories = w_tree.get_widget("categories")
        self.liststore = gtk.ListStore(str)

        for category in category_names_by_id.values():
            self.liststore.append([category])
        categories.set_model(self.liststore)
        categories.set_text_column(0)
        if category_names_by_id.values():
            categories.get_child().set_text(category_names_by_id.values()[0])

    def add_card_cb(self, widget):
        """ Add card to database """

        try:
            fact_data = self.get_data()
        except ValueError:
            return # Let the user try again to fill out the missing data.

        # Create new card
        main = ui_controller_main()
        main.create_new_cards(fact_data, self.card_type, 5,
            [self.categories.get_child().get_text()])

        database().save(config()['path'])

        #FIX ME need checking for success for previous operations
        self.clear_data_widgets()


    def add_card2_cb(self, widget, event):
        """ Hook for add_card for eventboxes """

        self.add_card_cb (widget)

    def get_data(self, check_for_required=True):
        """ Get data from widgets """

        fact = {}
        for edit_box, fact_key in self.edit_boxes.iteritems():
            start, end = edit_box.get_buffer().get_bounds()
            fact[fact_key] = edit_box.get_buffer().get_text(start, end)

        if not check_for_required:
            return fact
        for required in self.card_type.required_fields():
            if not fact[required]:
                raise ValueError
        return fact

    def clear_data_widgets(self):
        """ Clear data in widgets """

        self.edit_boxes = {}

        #FIX ME It may work more faster if I make clearing only edit_box

        #Destroy fields_container 
        if self.fields_container:
            self.fields_container.destroy()

        #Prepare fields_container
        parent_fields_container = \
            self.w_tree.get_widget('fields_container_parent')
        self.fields_container = self.create_entries()
        parent_fields_container.pack_start(self.fields_container, 
            True, True, 0)


    def to_main_menu_cb(self, widget, event):
        """ Return to main menu """

        #Destroy fields_container
        if self.fields_container:
            self.fields_container.destroy()
        #Destroy categories entry
#        if self.listsore:
#            self.liststore.destroy()



class HildonUiControllerConfig(HildonBaseUi):
    """ Hildon Config controller """

    def __init__(self):
        """ Initialization items of config window """
        HildonBaseUi.__init__(self,  signals=
            ['change_fullscreen', 'change_font_size','change_startup_with_review'])
        self.modified = False
        self.configuration = config()

    def start(self, w_tree):
        """ Start config window """
        self.w_tree = w_tree
        HildonBaseUi.start(self, w_tree)
        self.checkbox_fullscreen_mode.set_active(
            self.configuration['fullscreen'])
        self.checkbox_start_in_review_mode.set_active(
            self.configuration['startup_with_review'])
        self.spinbutton_fontsize.set_value(self.configuration['font_size'])
        self.switcher.set_current_page(self.config)

    def change_fullscreen_cb(self, widget):
        """ Change Fullscreen parameter """
        self.modified = True
        self.configuration['fullscreen'] = self.checkbox_fullscreen_mode.get_active()

    def change_font_size_cb(self, widget):
        self.modified = True
        self.configuration['font_size'] = self.spinbutton_fontsize.get_value_as_int()

    def change_startup_with_review_cb(self, widget):
        self.modified = True
        self.configuration['startup_with_review'] = self.checkbox_start_in_review_mode.get_active()

    def to_main_menu_cb(self, widget, event):
        if self.modified:
            self.configuration.save()
        self.switcher.set_current_page(self.main_menu)



class EternalControllerReview(HildonUiControllerReview):
    """ Eternal UI review controller """

    def __init__(self):
        self.base = HildonUiControllerReview
        self.base.__init__(self)

    def new_question(self, learn_ahead=False):
        """ Show new question. Make get_answer_box visible """

        self.base.new_question(self, learn_ahead)
        self.get_answer_box.set_property('visible', True)
        self.grades.set_property('visible', False)
        self.answer_box.set_property('visible', False)

    def show_answer(self):
        """ Show answer. Make grades and answer_box visible """

        self.base.show_answer(self)
        self.get_answer_box.set_property('visible', False)
        self.grades.set_property('visible', True)
        self.answer_box.set_property('visible', True)



class HildonUiControllerMain(HildonBaseUi):
    """ Hidon Main Controller  """

    def __init__(self, signals=None):
        HildonBaseUi.__init__(self, signals)

    def edit_current_card(self):
        """ Not Implemented Yet """

        pass

    def update_related_cards(self, fact, new_fact_data, new_card_type, \
                             new_cat_names):
        """ Not Implemented """

        pass


    def file_new(self):
        """ Not Implemented Yet """

        pass

    def file_open(self):
        """ Not Implemented Yet """

        pass

    def file_save(self):
        """ Not Implemented Yet """

        pass

    def file_save_as(self):
        """ Not Implemented Yet """

        pass


class EternalControllerMain(HildonUiControllerMain):
    """ Eternal UI Main Controller """

    def __init__(self):
        """ Added spliter widget to class """

        self.base = HildonUiControllerMain
        self.base.__init__(self, ["size_allocate"])
        self.spliter_trigger = True

    def start(self, w_tree):
        """ Start base class """
        HildonBaseUi.start(self, w_tree)

    def size_allocate_cb(self, widget, user_data):
        """ Checking window size """

        if (self.switcher.get_current_page() == self.review):
            if (self.spliter_trigger):
                # Set Spliter (GtkVpan) to pseudo medium
                self.spliter_trigger = False
                pseudo_medium = (widget.allocation.height - 70)/2 - 20
                self.spliter.set_property('position', pseudo_medium)
            else:
                self.spliter_trigger = True


class EternalControllerConfigure(HildonUiControllerConfig):
    """ Eternal UI Controller Configure """
    pass


class SmileControllerMain(HildonUiControllerMain):
    """ Smile UI Main Controller """

    pass


class SmileControllerReview(HildonUiControllerReview):
    """ Smile UI Review Controller """

    pass


class DraftControllerMain(HildonUiControllerMain):
    """ Draft UI Main Controller """

    pass


class DraftControllerReview(HildonUiControllerReview):
    """ Draft UI Review Controller """

    pass

class EternalControllerInput(HildonUiControllerInput):
    """ Eteranl UI Input Controller """

    pass

class SmileControllerInput(HildonUiControllerInput):
    """ Smile UI Input Controller """
    pass


class HildonUI():
    """ Hildon UI """

    def __init__(self, controllers):

        def gen_callback(mode):
            """Generate callback for mode."""
            def callback(widget, event = None):
                """Callback function."""
                self.controllers[mode].start(self.w_tree)
            return callback

        ui_controller_main().widget = self
        theme_path = config()["theme_path"]
        gtk.rc_parse(os.path.join(theme_path, "rcfile"))
        gtk.glade.set_custom_handler(self.custom_handler)
        self.w_tree = gtk.glade.XML(os.path.join(theme_path, "window.glade"))

        # Set unvisible tabs of switcher
        switcher = self.w_tree.get_widget("switcher")
        switcher.set_property('show_tabs', False)
        self.window = self.w_tree.get_widget("window")
        self.window.connect('delete_event', gtk.main_quit)

        # fullscreen mode
        if config()['fullscreen']:
            self.window.fullscreen()
            self.fullscreen = True
        else:
            self.fullscreen = False

        # Generate callbacks for modes
        self.controllers = controllers
        signals = ["review", "input", "configure"]
        for signal in signals:
            setattr(self, signal + '_cb', gen_callback(signal))

        self.signals = ["exit", "window_state", "window_keypress"] + signals

        # connect signals to methods
        self.w_tree.signal_autoconnect(dict([(sig, getattr(self, sig + "_cb")) \
            for sig in self.signals]))

    def start(self, mode):
        """ Start UI  """

        self.controllers[mode].start(self.w_tree)
        
        # start in review mode
        #if config()['startup_with_review']:
        #    mode = "review"

        self.controllers[mode].start(self.w_tree)
        gtk.main()

    def custom_handler(self, glade, function_name, widget_name, *args):

        """ Hook for custom widgets """

        if glade and widget_name and  hasattr(self, function_name):
            handler = getattr(self, function_name)
            return handler(args)

    # Callbacks

    @staticmethod
    def exit_cb(widget):
        """ If pressed quit button then close the window """

        gtk.main_quit()


    def window_keypress_cb(self, widget, event, *args):
        """ Key pressed """

        if event.keyval == gtk.keysyms.F6:
            # The "Full screen" hardware key has been pressed
            if self.fullscreen:
                self.window.unfullscreen()
                self.fullscreen = False
            else:
                self.window.fullscreen()
                self.fullscreen = True

    def window_state_cb(self, widget, event):
        """ Checking window state """

        self.fullscreen = bool(event.new_window_state & \
            gtk.gdk.WINDOW_STATE_FULLSCREEN)


    @staticmethod
    def create_gtkhtml(args):
        """ Create gtkhtml2 widget """


        view = gtkhtml2.View()
        document = gtkhtml2.Document()
        view.set_document(document)
        view.document = document
        view.show()
        return view

    @staticmethod
    def information_box(message, ok_string):
        """ Create Information message """

        #FIX ME Need glade window
        message_window = gtk.MessageDialog(None,
            gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO,
            gtk.BUTTONS_OK, message)
        message_window.run()
        message_window.destroy()

    @staticmethod
    def question_box(question, option0, option1, option2):
        """ Create Question message """

        print question, option0, option1, option2
        #FIX ME Need glade window
        question_window = gtk.MessageDialog(None, 
            gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_QUESTION, 
            gtk.BUTTONS_YES_NO, question)
        response = question_window.run()
        question_window.destroy()

        if response == gtk.RESPONSE_YES:
            return False
        else:
            return True

    def update_status_bar(self, message=None):
        """ Not Implemented """

        pass


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
