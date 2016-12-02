"""
Request and Response
====================

Request
-------

When a page is requested, automatically created a :class:`Request` object that
contains metadata about the request.
Since this object is global within the thread,
you can freely import from anywhere and retrieve request information.


Response
--------

In contrast to :class:`Request` objects, which are created automatically,
:class:`Response` objects are your responsibility.
Each view functions you write is responsible
for instantiating and returning an :class:`Response` or its child classes.

In addition to the :class:`Response` class, Kobin provides :class:`TemplateResponse` ,
 :class:`JSONResponse` , :class:`RedirectResponse` and :class:`HTTPError`.
"""
import threading
import cgi
import json
import http.client as http_client
from urllib.parse import SplitResult, urljoin
from http.cookies import SimpleCookie
from wsgiref.headers import Headers


##################################################################################
# Request Object #################################################################
##################################################################################
class Request:
    """ A wrapper for WSGI environment dictionaries.
    """
    __slots__ = ('environ', '_body', )

    def __init__(self, environ=None):
        self.environ = {} if environ is None else environ
        self.environ['kobin.request'] = self
        self._body = None

    def get(self, value, default=None):
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

    @property
    def GET(self):
        params = cgi.FieldStorage(
            environ=self.environ,
            keep_blank_values=True,
        )
        p = {k: params[k].value for k in params}
        return p

    @property
    def POST(self):
        form = cgi.FieldStorage(
            fp=self.environ['wsgi.input'],
            environ=self.environ,
            keep_blank_values=True,
        )
        params = {k: form[k].value for k in form}
        return params

    @property
    def body(self):
        if self._body is None:
            self._body = self.environ['wsgi.input'].read(int(self.environ.get('CONTENT_LENGTH', 0))).decode('utf-8')
        return self._body

    @property
    def json(self):
        return json.loads(self.body)

    @property
    def url(self):
        protocol = self.get('HTTP_X_FORWARDED_PROTO') or self.get('wsgi.url_scheme', 'http')
        host = self.get('HTTP_X_FORWARDED_HOST') or self.get('HTTP_HOST')
        query_params = self.get("QUERY_STRING")
        url_split_result = SplitResult(protocol, host, self.path, query_params, '')
        return url_split_result.geturl()

    @property
    def cookies(self):
        cookies = SimpleCookie(self.environ.get('HTTP_COOKIE', '')).values()
        return {c.key: c.value for c in cookies}

    def get_cookie(self, key, default=None, secret=None):
        value = self.cookies.get(key)
        return value or default

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
    bind = Request.__init__
    environ = _local_property()
    _body = _local_property()


request = LocalRequest()

##################################################################################
# Response Object ################################################################
##################################################################################

HTTP_CODES = http_client.responses.copy()
_HTTP_STATUS_LINES = dict((k, '%d %s' % (k, v)) for (k, v) in HTTP_CODES.items())


class Response:
    """"""
    default_status = 200
    default_content_type = 'text/plain; charset=UTF-8'

    def __init__(self, body='', status=None, headers=None, charset='utf-8'):
        self.headers = Headers()
        self._body = body
        self._status_code = status or self.default_status
        self._cookies = SimpleCookie()
        self.charset = charset

        if headers:
            for name, value in headers.items():
                self.headers.add_header(name, value)

    @property
    def body(self):
        return [self._body.encode(self.charset)]

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
    def status(self, status_code):
        if not 100 <= status_code <= 999:
            raise ValueError('Status code out of range.')
        self._status_code = status_code

    @property
    def headerlist(self):
        """ WSGI conform list of (header, value) tuples. """
        if 'Content-Type' not in self.headers:
            self.headers.add_header('Content-Type', self.default_content_type)
        if self._cookies:
            for c in self._cookies.values():
                self.headers.add_header('Set-Cookie', c.OutputString())
        return self.headers.items()

    def set_cookie(self, key, value, expires=None, path=None, **options):
        from datetime import timedelta, datetime, date
        import time
        self._cookies[key] = value
        if expires:
            self._cookies[key]['expires'] = expires
        if path:
            self._cookies[key]['path'] = path

        for k, v in options.items():
            if k == 'max_age':
                if isinstance(v, timedelta):
                    v = v.seconds + v.days * 24 * 3600
            if k == 'expires':
                if isinstance(v, (date, datetime)):
                    v = v.timetuple()
                elif isinstance(v, (int, float)):
                    v = v.gmtime(value)
                v = time.strftime("%a, %d %b %Y %H:%M:%S GMT", v)
            self._cookies[key][k.replace('_', '-')] = v

    def delete_cookie(self, key, **kwargs):
        kwargs['max_age'] = -1
        kwargs['expires'] = 0
        self.set_cookie(key, '', **kwargs)


class JSONResponse(Response):
    """Returns a html using jinja2 template engine"""
    default_content_type = 'application/json; charset=UTF-8'

    def __init__(self, dic, status=200, headers=None, charset='utf-8', **dump_args):
        self.dic = dic
        self.json_dump_args = dump_args
        super().__init__('', status=status, headers=headers, charset=charset)

    @property
    def body(self):
        return [json.dumps(self.dic, **self.json_dump_args).encode(self.charset)]


class TemplateResponse(Response):
    """Returns a JSON text from dict or OrderedDict."""
    default_content_type = 'text/html; charset=UTF-8'

    def __init__(self, filename, status=200, headers=None, charset='utf-8', **tpl_args):
        from . import current_config
        self.template = current_config()['JINJA2_ENV'].get_template(filename)
        self.tpl_args = tpl_args
        super().__init__(body='', status=status, headers=headers, charset=charset)

    @property
    def body(self):
        return [self.template.render(**self.tpl_args).encode(self.charset)]


class RedirectResponse(Response):
    """Redirect the specified url."""
    def __init__(self, url):
        status = 303 if request.get('SERVER_PROTOCOL') == "HTTP/1.1" else 302
        super().__init__('', status=status, headers={'Location': urljoin(request.url, url)})


class HTTPError(Response, Exception):
    """Return the error message when raise this class."""
    default_status = 500

    def __init__(self, body, status, headers=None, charset='utf-8'):
        super().__init__(body=body, status=status or self.default_status,
                         headers=headers, charset=charset)
