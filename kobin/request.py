import threading
from typing import Dict


class Request(object):
    """ A wrapper for WSGI environment dictionaries.
    """

    __slots__ = ('environ', )
    #: Maximum size of memory buffer for :attr:`body` in bytes.
    MEMFILE_MAX = 102400

    def __init__(self, environ: Dict=None):
        self.environ = {} if environ is None else environ
        self.environ['kobin.request'] = self

    def copy(self):
        """ Return a new :class:`Request` with a shallow :attr:`environ`
            copy. """
        return Request(self.environ.copy())

    def get(self, value: str, default=None):
        return self.environ.get(value, default)

    @property
    def path(self):
        """ The value of ``PATH_INFO`` with exactly one prefixed slash (to fix
            broken clients and avoid the "empty path" edge case). """
        return '/' + self.environ.get('PATH_INFO', '').lstrip('/')

    @property
    def method(self):
        """ The ``REQUEST_METHOD`` value as an uppercase string. """
        return self.environ.get('REQUEST_METHOD', 'GET').upper()

    def __getitem__(self, key):
        return self.environ[key]

    def __delitem__(self, key):
        self[key] = ""
        del (self.environ[key])

    def __setitem__(self, key, value):
        """ Change an environ value and clear all caches that depend on it. """
        self.environ[key] = value
        todelete = ()

        if key == 'wsgi.input':
            todelete = ('body', 'forms', 'files', 'params', 'post', 'json')
        elif key == 'QUERY_STRING':
            todelete = ('query', 'params')
        elif key.startswith('HTTP_'):
            todelete = ('headers', 'cookies')

        for key in todelete:
            self.environ.pop('kobin.request.' + key, None)

    def __len__(self):
        return len(self.environ)

    def keys(self):
        return self.environ.keys()

    def __repr__(self):
        return '<{cls}: {method} {url}>'.format(
            cls=self.__class__.__name__, method=self.method, url=self.path
        )


def _local_property():
    ls = threading.local()

    def fget(_):
        try:
            return ls.var
        except AttributeError:
            raise RuntimeError("Request context not initialized.")

    def fset(_, value):
        ls.var = value

    def fdel(_):
        del ls.var

    return property(fget, fset, fdel, 'Thread-local property')


class LocalRequest(Request):
    """ A thread local subclass of :class:`Request`
    """
    bind = Request.__init__
    environ = _local_property()


request = LocalRequest()
local = threading.local()
