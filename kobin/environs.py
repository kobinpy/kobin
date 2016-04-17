import threading
import cgi
from typing import Dict, List, Tuple
import http.client as http_client


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


##################################################################################
# Request Object #################################################################
##################################################################################

class Request:
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

    @property
    def GET(self):  # type: ignore
        params = cgi.FieldStorage(
            environ=self.environ,
            keep_blank_values=True,
        )
        return params

    @property
    def POST(self):  # type: ignore
        params = cgi.FieldStorage(
            fp=self.environ['wsgi.input'],
            environ=self.environ,
            keep_blank_values=True,
        )
        return params

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


class LocalRequest(Request):
    """ A thread local subclass of :class:`Request`
    """
    bind = Request.__init__
    environ = _local_property()


##################################################################################
# Response Object ################################################################
##################################################################################

HTTP_CODES = http_client.responses.copy()
_HTTP_STATUS_LINES = dict((k, '%d %s' % (k, v)) for (k, v) in HTTP_CODES.items())


class Response:
    default_status = 200
    default_content_type = 'text/html; charset=UTF-8'

    def __init__(self, body: str='', status: int=None, headers: Dict=None,
                 **more_headers) -> None:
        self._headers = {}  # type: Dict[str, List[str]]
        self.body = body
        self._status_code = status or self.default_status

        if headers:
            for name, value in headers.items():
                self.add_header(name, value)
        if more_headers:
            for name, value in more_headers.items():
                self.add_header(name, value)

    @property
    def status_code(self):
        """ The HTTP status code as an integer (e.g. 404)."""
        return self._status_code

    @property
    def status(self):
        """ The HTTP status line as a string (e.g. ``404 Not Found``)."""
        if not 100 <= self._status_code <= 999:
            raise ValueError('Status code out of range.')
        status = _HTTP_STATUS_LINES.get(self._status_code)
        return str(status or ('{} Unknown'.format(self._status_code)))

    @status.setter
    def status(self, status_code: int):
        if not 100 <= status_code <= 999:
            raise ValueError('Status code out of range.')
        self._status_code = status_code

    @property
    def headerlist(self) -> List[Tuple[str, str]]:
        """ WSGI conform list of (header, value) tuples. """
        out = []  # type: List[Tuple[str, str]]
        headers = list(self._headers.items())
        if 'Content-Type' not in self._headers:
            headers.append(('Content-Type', [self.default_content_type]))
        out += [(name, val)
                for (name, vals) in headers
                for val in vals]
        return [(k, v.encode('utf8').decode('latin1')) for (k, v) in out]

    def add_header(self, key: str, value: str) -> None:
        self._headers.setdefault(key, []).append(value)

    def apply(self, other):
        self.status = other._status_code
        self._headers = other._headers
        self.body = other.body


class LocalResponse(Response):
    """ A thread-local subclass ob :class:`BaseResponse` with a different set
        of attributes for each thread
    """
    bind = Response.__init__
    _status_code = _local_property()
    _headers = _local_property()
    body = _local_property()


##################################################################################
# Make Request and Response object to thread local ###############################
##################################################################################

request = LocalRequest()  # type: LocalRequest
response = LocalResponse()  # type: LocalResponse
local = threading.local()  # type: ignore
