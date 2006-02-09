"""Stubs for module 'gtk'."""

# A marker that may be used in application unit tests as a sanity check.
_fake_module = True

from real_gtk import *
from gtktest import gtkinfo
import real_gdk as gdk

# We should import fake_glade as glade here to make 'import gtk.glade' work
# as expected, but we can not do that because it introduces a circular import.
# See workaround at the end of gtktest/__init__.py.


def main():
    mainhook = gtkinfo.main
    if mainhook is None:
        raise ValueError("mainhook not specified!")
    else:
        gtkinfo.main = None # try to avoid infinite recursion
        gtkinfo.level += 1
        mainhook()


def main_quit():
    gtkinfo.level -= 1

# deprecated alternatives
mainloop = main
mainquit = main_quit


#
# Some mutilated GTK classes to suppress side effects
#


class _InvisibleWidgetMixin(object):
    """A mixin that can be used to try to stop widgets from appearing onscreen.

    Its attribute `_visible` (None by default) is set to True if the widget's
    show() method or friends are called, False if hide() or friends are called.
    """

    _visible = None

    def show(self):
        self._visible = True

    def hide(self):
        self._visible = False

    show_now = show
    show_all = show
    hide_all = hide


class Window(_InvisibleWidgetMixin, Window):
    pass


class Dialog(_InvisibleWidgetMixin, Dialog):

    def run(self):
        """Run the dialog and return a user-specified value.

        Invokes callable gtkinfo.dlg_handler with the dialog instance
        as a single argument and returns the handler's return value as
        the response.
        """
        assert gtkinfo.dlg_handler, 'dlg_handler not set'
        handler = gtkinfo.dlg_handler
        gtkinfo.dlg_handler = None
        response = handler(self)
        assert response is not None, 'dlg_handler returned None'
        return response
