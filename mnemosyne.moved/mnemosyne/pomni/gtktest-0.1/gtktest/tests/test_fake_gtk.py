"""Tests for the fake_gtk module."""

import unittest
import doctest
import sys

from gtktest import doctest_setUp, doctest_tearDown, gtkinfo
from gtktest.fake_gtk import Window, Dialog


def test_Window():
    """Tests for the overridden Window class.

    show() and hide() should set `_visible`.

        >>> w = Window()
        >>> print w._visible
        None
        >>> w.show()
        >>> w._visible
        True

    The window has not been really shown:

        >>> w.get_property('visible')
        False

    hide() is also handled:

        >>> w.hide()
        >>> w._visible
        False

    Associated methods: show_now(), show_all(), hide_all()

        >>> w.show_now()
        >>> w._visible
        True
        >>> w.get_property('visible')
        False

        >>> w.hide_all()
        >>> w._visible
        False

        >>> w.show_all()
        >>> w._visible
        True
        >>> w.get_property('visible')
        False

    """

def test_Dialog():
    """Tests for the overridden Dialog class.

    Dialogs, like Windows, should never be really shown:

        >>> dlg = Dialog()
        >>> dlg.show()
        >>> dlg._visible
        True
        >>> dlg.get_property('visible')
        False

    First, if we invoke Dialog.run() without any other settings, we get an
    assertion error:

        >>> dlg = Dialog()
        >>> dlg.run()
        Traceback (most recent call last):
            ...
        AssertionError: dlg_handler not set

    We have to set gtkinfo.dlg_handler:

        >>> def sample_handler(dialog):
        ...     if dialog is dlg:
        ...         print 'Parameter correct'
        ...     return 'cancel'
        >>> gtkinfo.dlg_handler = sample_handler

        >>> response = dlg.run()
        Parameter correct
        >>> response
        'cancel'

    You can deal with consecutive dialogs by assigning the next handler to
    dlg_handler inside the running one.

        >>> def handler1(dialog):
        ...     gtkinfo.dlg_handler = handler2
        ...     return 1
        >>> def handler2(dialog):
        ...     return 2
        >>> gtkinfo.dlg_handler = handler1

        >>> dlg.run()
        1
        >>> dlg.run()
        2

    glade has to substitute dialogs from XML with proxies whose run()
    method behaves similarly.

        >>> from gtktest.fake_gtk.fake_glade import XML
        >>> import os
        >>> path = os.path.dirname(__file__)
        >>> f = open(os.path.join(path, 'sample.glade'))
        >>> tree = XML(os.path.join(path, 'sample.glade'))
        >>> dlg = tree.get_widget('dialog')
        >>> dlg.get_title()
        'Sample dialog'
        >>> gtkinfo.dlg_handler = lambda dialog: 'glade'
        >>> dlg.run()
        'glade'

    """


def test_suite():
    docsuite = doctest.DocTestSuite(optionflags=doctest.ELLIPSIS)
    return unittest.TestSuite([docsuite])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
