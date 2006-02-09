"""Tests for the gtkstubs module."""

import unittest
import doctest
import sys

from gtktest import GtkTestHelperMixin, doctest_setUp, doctest_tearDown
from gtktest import doctest_setUp_param, gtkinfo
import gtk
import real_gtk


def doctest_GtkTestHelperMixin():
    """Tests for GtkTestHelperMixin.

    First, let's make sure that setUp & tearDown does not fail with no options
    specified:

        >>> helper = GtkTestHelperMixin()
        >>> helper.setUp()

        >>> helper._original
        []
        >>> helper.tearDown()

    In the next step we will need a module (which we simulate by using a
    class):

        >>> class ModuleStub(object):
        ...     obj = "original"
        ...     class Logged(object):
        ...         def noop(self, arg): pass
        >>> module = sys.modules['_override_test'] = ModuleStub

    Let's try overriding the obj attribute.  We use a string to make it easier
    to test, but in reality this will usually be a function or a class.

        >>> helper = GtkTestHelperMixin()
        >>> helper.overrides = {'_override_test.obj': "overridden"}
        >>> helper.logging = {'_override_test.Logged': ['noop']}
        >>> helper.setUp()

    The attribute has been overridden:

        >>> module.obj
        'overridden'

    Logging works:

        >>> module.Logged().noop('foo')
        >>> gtkinfo.calls
        [(<...Logged object...>, 'noop', ('foo',), {})]

    The original objects have been stored in the attribute _original.

        >>> len(helper._original)
        2
        >>> helper._original[0]
        (<...ModuleStub...>, 'obj', 'original')
        >>> helper._original[1]
        (<...Logged...>, 'noop', <unbound method Logged.noop>)

    tearDown should put things back into their places:

        >>> helper.tearDown()
        >>> gtkinfo.calls = []

        >>> module.obj
        'original'
        >>> module.Logged().noop('foo')
        >>> gtkinfo.calls
        []

    Let's clean up:

        >>> del sys.modules['_override_test']

    """

def doctest_GtkTestHelperMixin_override():
    """Tests for overriding in GtkTestHelperMixin.

    A more thorough test for _override(): we will use a module hierarchy
    (simulated by nested classes):

        >>> class ModuleStub(object):
        ...     class sub(object):
        ...         class subsub(object):
        ...             obj = 'original'
        >>> module = sys.modules['_override_test'] = ModuleStub

        >>> helper = GtkTestHelperMixin()
        >>> helper._original = []
        >>> helper._override('_override_test.sub.subsub.obj', 'overridden')
        >>> module.sub.subsub.obj
        'overridden'

    _override() will create an object if it's not there:

        >>> helper._override('_override_test.sub.subsub.another', 'new')
        >>> module.sub.subsub.another
        'new'

    tearDown should restore 'obj' and delete 'another':

        >>> helper.tearDown()
        >>> module.sub.subsub.obj
        'original'
        >>> module.sub.subsub.another
        Traceback (most recent call last):
            ...
        AttributeError: type object 'subsub' has no attribute 'another'

    Final test: _override should be able to handle static classes, i.e.,
    classes whose attributes can not be set.  This applies to most GTK widgets,
    because they come from a C extension.  We then create a class that inherits
    from them and add our methods there.

        >>> class ModuleStub(object):
        ...     Entry = real_gtk.Entry
        >>> module = sys.modules['_override_test'] = ModuleStub

        >>> helper = GtkTestHelperMixin()
        >>> helper._original = []
        >>> def fake_show(self): print "showing"
        >>> helper._override('_override_test.Entry.show', fake_show)
        >>> helper._override('_override_test.Entry.new_attr', 'new')

        >>> e = module.Entry()
        >>> e.show()
        showing
        >>> e.new_attr
        'new'

    tearDown works properly here too:

        >>> helper._original
        [(<class '...ModuleStub'>, 'Entry', <type 'gtk.Entry'>), \
(<class 'gtktest.Entry'>, 'new_attr', None)]

        >>> helper.tearDown()
        >>> e = module.Entry()
        >>> e.show()
        >>> e.new_attr
        Traceback (most recent call last):
            ...
        AttributeError: 'gtk.Entry' object has no attribute 'new_attr'

    Let's clean up:

        >>> del sys.modules['_override_test']

    """


def doctest_GtkTestHelperMixin_logging():
    """Tests for automatic logging support in GtkTestHelperMixin.

        >>> helper = GtkTestHelperMixin()
        >>> class ModuleStub(object):
        ...     class SomeObj(object):
        ...         def hello(self, name, dot=True):
        ...             print 'hello,', name + (dot and '.' or '')
        >>> module = sys.modules['_override_test'] = ModuleStub
        >>> helper._original = []
        >>> helper._logCalls('_override_test.SomeObj')

        >>> o = module.SomeObj()
        >>> o.hello('gintas')
        hello, gintas.
        >>> o.hello('ignas', dot=False)
        hello, ignas

        >>> len(gtkinfo.calls)
        2
        >>> gtkinfo.calls[0][1:]
        ('hello', ('gintas',), {})
        >>> gtkinfo.calls[0][0] is o
        True
        >>> gtkinfo.calls[1][1:]
        ('hello', ('ignas',), {'dot': False})
        >>> gtkinfo.calls[1][0] is o
        True

    Let's clear the fixture for the next experiment:

        >>> helper.tearDown()

    We will now try attaching a logger to a C extension class:

        >>> helper = GtkTestHelperMixin()
        >>> helper._original = []
        >>> helper._logCalls('gtk.Entry', ['hide'])
        >>> entry = gtk.Entry()
        >>> entry.hide()
        >>> gtkinfo.calls
        [(<Entry object ...>, 'hide', (), {})]

    Clean up:

        >>> del sys.modules['_override_test']

    """


def doctest_GtkTestHelperMixin_resolvePath():
    """Tests for GtkTestHelperMixin._resolvePath.

        >>> helper = GtkTestHelperMixin()
        >>> def resolvePath(path):
        ...     path = path.split('.')
        ...     for obj in helper._resolvePath(path):
        ...         print repr(obj)

        >>> resolvePath('gtk')
        <module 'gtktest.fake_gtk' ...>

        >>> resolvePath('gtk.glade')
        <module 'gtktest.fake_gtk' ...>
        <module 'gtktest.fake_gtk.fake_glade' ...>

        >>> resolvePath('gtktest.tests.test_gtkstubs.test_suite')
        <module 'gtktest' ...>
        <module 'gtktest.tests' ...>
        <module 'gtktest.tests.test_gtkstubs' ...>
        <function test_suite at ...>

        >>> resolvePath('gtk.nonexistent')
        Traceback (most recent call last):
            ...
        ImportError: No module named nonexistent

    """


def doctest_doctest_support():
    """Tests for doctest convenience functions.

    First, no overrides:

        >>> doctest_setUp()

        >>> import gtktest
        >>> gtktest.doctestmgr.overrides
        {}

        >>> doctest_tearDown()
        >>> print gtktest.doctestmgr
        None

    Let's add a few overrides and logging.  We will have to use the
    more complex form.

        >>> overrides = {'gtk.Entry.something': 'new'}
        >>> logging = {'gtk.Entry': ['show', 'hide']}
        >>> setup = doctest_setUp_param(overrides=overrides, logging=logging)
        >>> setup()

        >>> import gtktest
        >>> gtktest.doctestmgr.overrides
        {'gtk.Entry.something': 'new'}
        >>> gtktest.doctestmgr.logging
        {'gtk.Entry': ['show', 'hide']}

        >>> doctest_tearDown()
        >>> print gtktest.doctestmgr
        None

    """


def test_suite():
    suite = doctest.DocTestSuite(optionflags=doctest.ELLIPSIS)
    return unittest.TestSuite([suite])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
