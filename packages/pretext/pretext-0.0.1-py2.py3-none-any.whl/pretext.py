from __future__ import print_function

try:
    import reprlib
except ImportError:
    import repr as reprlib

import sys

__all__ = [
    'PrefixRepr',
]


class PrefixRepr(reprlib.Repr):
    """A Repr variant that always prefixes bytes/str/unicode literals
    """
    def __init__(self):
        self._old_repr = repr

        self.maxlevel = sys.maxsize
        self.maxdict = sys.maxsize
        self.maxlist = sys.maxsize
        self.maxset = sys.maxsize
        self.maxfrozenset = sys.maxsize
        self.maxdeque = sys.maxsize
        self.maxarray = sys.maxsize
        self.maxlong = sys.maxsize
        self.maxstring = sys.maxsize
        self.maxother = sys.maxsize

    def repr_str(self, obj, level):
        """Return the repr of a string, prefixed with b or u
        """
        if str is bytes:
            # Python 2.x
            return b'b%s' % (self._old_repr(obj),)
        else:
            # Python 3.x
            return u'u%s' % (self._old_repr(obj),)

