from real_glade import *
from real_glade import XML as _RealXML
from real_gtk import Dialog, Window
from gtktest import fake_gtk


class _ProxyMixin(object):
    """Mixin for use in proxy classes.

    Note that use of this mixin breaks isinstance() for proxied widgets.
    You're better off not trying to add them to other containers by hand, etc.
    """

    _overrides = ()

    def __init__(self, obj):
        self._obj = obj

    def __getattr__(self, name):
        return getattr(self._obj, name)


def _createProxy(clsname, overrides):
    fakeclass = getattr(fake_gtk, clsname)
    cls_dict = {}
    for name in overrides:
        cls_dict[name] = getattr(fakeclass, name).im_func
    return type(clsname, (_ProxyMixin, ), cls_dict)



_DialogProxy = _createProxy('Dialog', ['run', 'show', 'show_all'])
_WindowProxy = _createProxy('Window', ['show', 'show_all'])


class XML(_RealXML):

    def get_widget(self, name):
        widget = _RealXML.get_widget(self, name)
        if isinstance(widget, Dialog):
            return _DialogProxy(widget)
        elif isinstance(widget, Window):
            return _WindowProxy(widget)
        else:
            return widget
