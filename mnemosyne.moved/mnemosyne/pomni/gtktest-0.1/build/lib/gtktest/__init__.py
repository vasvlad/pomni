"""A collection of stubs for GTK objects for use in unit tests."""

import sys
import unittest
import types


class Info(object):
    """A singleton that stores miscellaneous info about the GTK fixture."""

    def __init__(self):
        self.reset()

    def reset(self):
        self.main = None
        self.level = 0 # number of recursive main() calls
        self.dlg_handler = None
        self.dlg_response = None
        self.calls = []


gtkinfo = Info()


class GtkTestHelperMixin(object):
    """A class for use in setting up or tearing down GTK test fixtures.

    This class does not inherit from unittest.TestCase because it is used
    both in unittest and doctest setup.
    """

    # to be overridden in subclasses
    overrides = {}
    logging = {}

    def setUp(self):
        gtkinfo.reset()
        self._original = []
        for name, obj in self.overrides.items():
            self._override(name, obj)
        for name, obj in self.logging.items():
            self._logCalls(name, obj)

    def _resolvePath(self, path):
        """Transform a sequence of identifiers to a sequence of objects.

        'path' is a sequence of strings, that, when connected with dots,
        would form a python dot-path.  The function returns a sequence
        of objects of the same length.  An exception is raised if the
        path is invalid.
        """
        obj = __import__(path[0])
        objs = [obj]
        fullpath = path[0]
        for name in path[1:]:
            fullpath += '.' + name
            if not hasattr(obj, name):
                __import__(fullpath) # not very clean, but seems to work
            obj = getattr(obj, name)
            objs.append(obj)
        return objs

    def _override(self, name, obj):
        """Override object identified by a dot-separated path with 'obj'.

        This method relies on the fact that all modules have their submodules
        as attribute, e.g., if I have the module 'gtk', I can always find
        'gtk.glade' by getattr(gtk, 'glade').

        TODO: this could be usable on any modules, not just ones from our
        fake GTK, so it would be a good idea to lift this restriction.
        """
        path = name.split('.')
        assert len(path) > 1, 'module name not provided'
        obj_name = path[-1]

        objs = self._resolvePath(path[:-1])
        container = objs[-1]
        try:
            original_class = getattr(container, obj_name, None)
            setattr(container, obj_name, obj)
            self._original.append((container, obj_name, original_class))
        except TypeError:
            # We have a static class; we will have to modify its container.
            # This works for global functions in gtk too because their
            # container is an ordinary python module (fake_gtk).
            name = container.__name__
            prev_container = objs[-2]
            subclass = type(name, (container, ), {obj_name: obj})
            setattr(prev_container, name, subclass)
            self._original.append((prev_container, name, container))

    def _logCalls(self, dot_path, methods=None):
        """Add a logger to methods in class identified by dot_path.

        The list of methods can be supplied as the 'methods' argument.  If it
        is not provided, all methods are registered for logging.

        TODO: Make this work for top-level functions too.
        """
        path = dot_path.split('.')
        assert len(path) > 1, 'module name not provided'

        cls = self._resolvePath(path)[-1]
        if not methods:
            # Iterate through all methods except the special ones which
            # cause trouble...
            methods = [name for name in dir(cls)
                       if (not name.startswith('__')
                           and callable(getattr(cls, name)))]
        for name in methods:
            orig_method = getattr(cls, name)
            def new_method(self, *args, **kwargs):
                gtkinfo.calls.append((self, name, args, kwargs))
                return orig_method(self, *args, **kwargs)
            self._override(dot_path + '.' + name, new_method)

    def tearDown(self):
        gtkinfo.reset()
        for parent, name, obj in self._original:
            if obj is not None:
                setattr(parent, name, obj)
            else:
                delattr(parent, name)


class GtkTestCase(GtkTestHelperMixin, unittest.TestCase):
    """A convenience TestCase for use in GTK application unit tests."""


#
# Doctest support functions
#
# Example of use: suite = doctest.DocTestSuite(setUp=doctest_setUp,
#                                              tearDown=doctest_tearDown,
#                                              optionflags=doctest.ELLIPSIS)
#
# Note: these are only usable on Python 2.4 version of the doctest module.
#

doctestmgr = None

def doctest_setUp_param(overrides={}, logging={}):
    """Parametrized setUp for doctests."""
    def setup(test=None):
        global doctestmgr
        doctestmgr = GtkTestHelperMixin()
        doctestmgr.overrides = overrides
        doctestmgr.logging = logging
        doctestmgr.setUp()
    return setup # we were called to get a setUp function

def doctest_setUp(test=None):
    """Plain setUp as a convenience function for doctests."""
    setUp = doctest_setUp_param()
    setUp(test)

def doctest_tearDown(test=None):
    """tearDown for doctests."""
    global doctestmgr
    assert doctestmgr is not None, "doctest setup not invoked!"
    doctestmgr.tearDown()
    doctestmgr = None


#
# Miscellaneous
#

def mainloop_handler(app_main):
    """A helper for unit-test methods running instead of the main loop.

    This function takes as an argument the function which invokes gtk.main().
    A decorator for TestCase methods is returned.  In Python 2.4 you can
    use this helper like this:

        @mainloop_helper(my_app.main)
        def test_myApp(self):
            ...

    If you need to preserve compatibility with Python 2.3, you will not
    be able to use the decorator syntax:

        def test_myApp(self):
            ...
        test_myApp = mainloop_helper(my_app.main)(test_myApp)

    """
    # XXX No unit tests.
    def decorator(method):
        def proxy(self):
            """Run the application and then the test."""
            global gtkinfo
            gtkinfo.main = lambda: method(self)
            app_main()
        return proxy
    return decorator


#
# Module setup
#

# Save original modules
import gobject, pango, gtk.glade, gtk.gdk
sys.modules['real_gtk'] = sys.modules['gtk']
sys.modules['real_gobject'] = sys.modules['gobject']
sys.modules['real_pango'] = sys.modules['pango']
sys.modules['real_glade'] = sys.modules['gtk.glade']
sys.modules['real_gdk'] = sys.modules['gtk.gdk']

# Override original modules with fake ones.
from gtktest import fake_gtk, fake_gobject, fake_pango
sys.modules['gtk'] = fake_gtk
sys.modules['gobject'] = fake_gobject
sys.modules['pango'] = fake_pango

# Work around a circular import.
from gtktest.fake_gtk import fake_glade
fake_gtk.glade = fake_glade
