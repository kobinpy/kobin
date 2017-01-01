"""
Response
========

In contrast to :class:`Request` objects, which are created automatically,
:class:`Response` objects are your responsibility.
Each view functions you write is responsible
for instantiating and returning an :class:`Response` or its child classes.

In addition to the :class:`Response` class, Kobin provides :class:`TemplateResponse` ,
 :class:`JSONResponse` , :class:`RedirectResponse` and :class:`HTTPError`.
"""
import base64
import hashlib
import hmac
import time
import json
import pickle
import http.client as http_client
from urllib.parse import urljoin
from http.cookies import SimpleCookie
from wsgiref.headers import Headers

from .requests import request


HTTP_CODES = http_client.responses.copy()
_HTTP_STATUS_LINES = dict((k, '%d %s' % (k, v)) for (k, v) in HTTP_CODES.items())


class BaseResponse:
    """Base class for Response."""
    default_status = 200
    default_content_type = 'text/plain;'

    def __init__(self, body=None, status=None, headers=None):
        self._body = body if body else [b'']
        self._status_code = status or self.default_status
        self.headers = Headers()
        self._cookies = SimpleCookie()

        if headers:
            for name, value in headers.items():
                self.headers.add_header(name, value)

    @property
    def body(self):
        return self._body

    @property
    def status_code(self):
        """ The HTTP status code as an integer (e.g. 404)."""
        return self._status_code

    @property
    def status(self):
        """ The HTTP status line as a string (e.g. ``404 Not Found``)."""
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

    def set_cookie(self, key, value, expires=None, max_age=None, path='/',
                   secret=None, digestmod=hashlib.sha256):
        from kobin.app import current_config
        if secret is None:
            secret = current_config('SECRET_KEY')
        if secret:
            if isinstance(secret, str):
                secret = secret.encode('utf-8')
            encoded = base64.b64encode(pickle.dumps((key, value), pickle.HIGHEST_PROTOCOL))
            sig = base64.b64encode(hmac.new(secret, encoded, digestmod=digestmod).digest())
            value_bytes = b'!' + sig + b'?' + encoded
            value = value_bytes.decode('utf-8')

        self._cookies[key] = value
        if len(key) + len(value) > 3800:
            raise ValueError('Content does not fit into a cookie.')

        if max_age is not None:
            if isinstance(max_age, int):
                max_age_value = max_age
            else:
                max_age_value = max_age.seconds + max_age.days * 24 * 3600
            self._cookies[key]['max-age'] = max_age_value
        if expires is not None:
            if isinstance(expires, int):
                expires_value = expires
            else:
                expires_value = time.strftime("%a, %d %b %Y %H:%M:%S GMT", expires.timetuple())
            self._cookies[key]['expires'] = expires_value
        if path:
            self._cookies[key]['path'] = path

    def delete_cookie(self, key, **kwargs):
        kwargs['max_age'] = -1
        kwargs['expires'] = 0
        self.set_cookie(key, '', **kwargs)


class Response(BaseResponse):
    """Returns a plain text from unicode object."""
    default_content_type = 'text/plain; charset=UTF-8'

    def __init__(self, body='', status=None, headers=None, charset='utf-8'):
        if isinstance(body, str):
            body = body.encode(charset)
        iterable_body = [body]
        super().__init__(iterable_body, status, headers)
        self.charset = charset


class JSONResponse(BaseResponse):
    """Returns a HTML text from dict or OrderedDict."""
    default_content_type = 'application/json; charset=UTF-8'

    def __init__(self, dic, status=200, headers=None, charset='utf-8', **dump_args):
        body = [json.dumps(dic, **dump_args).encode(charset)]
        super().__init__(body, status=status, headers=headers)


class TemplateResponse(BaseResponse):
    """Returns a html using jinja2 template engine"""
    default_content_type = 'text/html; charset=UTF-8'

    def __init__(self, filename, status=200, headers=None, charset='utf-8', **tpl_args):
        from .app import current_config
        template_env = current_config('TEMPLATE_ENVIRONMENT')
        if template_env is None:
            raise HTTPError('TEMPLATE_ENVIRONMENT is not found in your config.')
        template = template_env.get_template(filename)
        body = [template.render(**tpl_args).encode(charset)]
        super().__init__(body, status=status, headers=headers)


class RedirectResponse(BaseResponse):
    """Redirect the specified url."""
    def __init__(self, url):
        status = 303 if request.get('SERVER_PROTOCOL') == "HTTP/1.1" else 302
        super().__init__([b''], status=status, headers={'Location': urljoin(request.url, url)})


class HTTPError(Response, Exception):
    """Return the error message when raise this class."""
    default_status = 500

    def __init__(self, body, status, headers=None, charset='utf-8'):
        super().__init__(body=body, status=status, headers=headers, charset=charset)
