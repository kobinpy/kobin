"""
Request
=======

When a page is requested, automatically created a :class:`Request` object that
contains metadata about the request.
Since this object is global within the thread,
you can freely import from anywhere and retrieve request information.
"""
import base64
import fnmatch
import hashlib
import hmac
import threading
import cgi
import json
import pickle
from urllib.parse import SplitResult
from http.cookies import SimpleCookie


##################################################################################
# Request Object #################################################################
##################################################################################


class Request:
    """ A wrapper for WSGI environment dictionaries.
    """
    __slots__ = ('environ', '_body', '_forms')

    def __init__(self, environ=None):
        self.environ = {} if environ is None else environ
        self.environ['kobin.request'] = self
        self._body = None
        self._forms = None

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
    def headers(self):
        return {k[len('HTTP_'):]: v
                for k, v in self.environ.items()
                if k.startswith('HTTP_')}

    @property
    def query(self):
        params = cgi.FieldStorage(
            environ=self.environ,
            keep_blank_values=True,
        )
        p = {k: params[k].value for k in params}
        return p

    @property
    def forms(self):
        if self._forms is None:
            form = cgi.FieldStorage(
                fp=self.environ['wsgi.input'],
                environ=self.environ,
                keep_blank_values=True,
            )
            self._forms = {k: form[k].value for k in form}
        return self._forms

    @property
    def raw_body(self):
        if self._body is None:
            self._body = self.environ['wsgi.input'].read(
                int(self.environ.get('CONTENT_LENGTH', 0)))
        return self._body

    @property
    def body(self):
        return self.raw_body.decode('utf-8')

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

    def get_cookie(self, key, default=None, secret=None, digestmod=hashlib.sha256):
        from kobin.app import current_config
        if secret is None:
            secret = current_config('SECRET_KEY')

        value = self.cookies.get(key)
        if secret and value and value.startswith('!') and '?' in value:
            # See BaseResponse.set_cookie for details.
            if isinstance(secret, str):
                secret = secret.encode('utf-8')
            sig, msg = map(lambda x: x.encode('utf-8'), value[1:].split('?', 1))
            hash_string = hmac.new(secret, msg, digestmod=digestmod).digest()
            if sig == base64.b64encode(hash_string):
                key_and_value = pickle.loads(base64.b64decode(msg))
                if key_and_value and key_and_value[0] == key:
                    return key_and_value[1]
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


# for Accept header.
def _split_into_mimetype_and_priority(x):
    """Split an accept header item into mimetype and priority.

    >>> _split_into_mimetype_and_priority('text/*')
    ('text/*', 1.0)

    >>> _split_into_mimetype_and_priority('application/json;q=0.5')
    ('application/json', 0.5)
    """
    if ';' in x:
        content_type, priority = x.split(';')
        casted_priority = float(priority.split('=')[1])
    else:
        content_type, casted_priority = x, 1.0

    content_type = content_type.lstrip().rstrip()  # Replace ' text/html' to 'text/html'
    return content_type, casted_priority


def _parse_and_sort_accept_header(accept_header):
    """Parse and sort the accept header items.

    >>> _parse_and_sort_accept_header('application/json;q=0.5, text/*')
    [('text/*', 1.0), ('application/json', 0.5)]
    """
    return sorted([_split_into_mimetype_and_priority(x) for x in accept_header.split(',')],
                  key=lambda x: x[1], reverse=True)


def accept_best_match(accept_header, mimetypes):
    """Return a mimetype best matched the accept headers.

    >>> accept_best_match('application/json, text/html', ['application/json', 'text/plain'])
    'application/json'

    >>> accept_best_match('application/json;q=0.5, text/*', ['application/json', 'text/plain'])
    'text/plain'
    """
    for mimetype_pattern, _ in _parse_and_sort_accept_header(accept_header):
        matched_types = fnmatch.filter(mimetypes, mimetype_pattern)
        if matched_types:
            return matched_types[0]
    return mimetypes[0]


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
    _forms = _local_property()


request = LocalRequest()
