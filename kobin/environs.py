import threading
from typing import Dict
import http.client as http_client

##################################################################################
# Request Object #################################################################
##################################################################################


class Request(object):
    """ A wrapper for WSGI environment dictionaries.
    """
    __slots__ = ('environ', )

    def __init__(self, environ: Dict=None) -> None:
        self.environ = {} if environ is None else environ
        self.environ['kobin.request'] = self

    def get(self, value: str, default=None):
        return self.environ.get(value, default)

    @property
    def path(self) -> str:
        """ The value of ``PATH_INFO`` with exactly one prefixed slash (to fix
            broken clients and avoid the "empty path" edge case). """
        return '/' + self.environ.get('PATH_INFO', '').lstrip('/')

    @property
    def method(self) -> str:
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

    def __repr__(self):
        return '<{cls}: {method} {url}>'.format(
            cls=self.__class__.__name__, method=self.method, url=self.path
        )


##################################################################################
# Response Object ################################################################
##################################################################################

HTTP_CODES = http_client.responses.copy()
_HTTP_STATUS_LINES = dict((k, '%d %s' % (k, v)) for (k, v) in HTTP_CODES.items())


class Response(object):
    default_status = 200
    default_content_type = 'text/html; charset=UTF-8'

    def __init__(self, body: str='', status: int=None, headers: Dict=None,
                 **more_headers) -> None:
        self._headers = {}
        self.body = body
        self.status = status or self.default_status

    @property
    def status_line(self):
        """ The HTTP status line as a string (e.g. ``404 Not Found``)."""
        return self._status_line

    @property
    def status_code(self):
        """ The HTTP status code as an integer (e.g. 404)."""
        return self._status_code

    def _set_status(self, status: int):
        code, status = status, _HTTP_STATUS_LINES.get(status)
        if not 100 <= code <= 999:
            raise ValueError('Status code out of range.')
        self._status_code = code
        self._status_line = str(status or ('%d Unknown' % code))

    def _get_status(self):
        return self._status_line

    status = property(_get_status, _set_status, None,
                      "A writable property to change the HTTP Response Status")
    del _get_status, _set_status


##################################################################################
# Make Request and Response object to thread local ###############################
##################################################################################


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


request = LocalRequest()  # type: LocalRequest
local = threading.local()  # type: ignore
