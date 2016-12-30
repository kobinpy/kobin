"""
Kobin class
===========

The Kobin instance are callable WSGI Application.

Usage
-----

.. code-block:: python

   from kobin import Kobin, Response
   app = Kobin()

   @app.route('/')
   def index() -> Response:
       return Response('Hello World')

"""
from importlib.machinery import SourceFileLoader
import os
import traceback

from .routes import Router
from .environs import request, HTTPError


class Kobin:
    """
    This class is a WSGI application implementation.
    Create a instance, and run using WSGI Server.
    """
    def __init__(self, config=None):
        self.router = Router()
        self.config = config if config else Config()
        self.before_request_callback = None
        self.after_request_callback = None

    def route(self, rule=None, method='GET', name=None, callback=None):
        def decorator(callback_func):
            self.router.add(method, rule, name, callback_func)
            return callback_func
        return decorator(callback) if callback else decorator

    def before_request(self, callback):
        def decorator(callback_func):
            self.before_request_callback = callback_func
            return callback_func
        return decorator(callback)

    def after_request(self, callback):
        def decorator(callback_func):
            self.after_request_callback = callback_func
            return callback_func
        return decorator(callback)

    def _handle(self, environ):
        environ['kobin.app'] = self
        request.bind(environ)

        try:
            if self.before_request_callback:
                self.before_request_callback()

            callback, kwargs = self.router.match(environ)
            response = callback(**kwargs) if kwargs else callback()

            if self.after_request_callback:
                wrapped_response = self.after_request_callback(response)
                if wrapped_response:
                    response = wrapped_response
        except HTTPError as e:
            response = e
        except BaseException as e:
            traceback.print_tb(e.__traceback__)
            if self.config['DEBUG']:
                message = '\n'.join(traceback.format_tb(e.__traceback__))
            else:
                message = 'Internal Server Error'
            response = HTTPError(message, 500)
        return response

    def wsgi(self, environ, start_response):
        response = self._handle(environ)
        start_response(response.status, response.headerlist)
        return response.body

    def __call__(self, environ, start_response):
        """It is called when receive http request."""
        return self.wsgi(environ, start_response)


class Config(dict):
    """This class manages your application configs.
    """
    def __init__(self, **kwargs):
        init_kw = {
            'BASE_DIR': os.path.abspath('.'),
            'TEMPLATE_DIRS': [os.path.join(os.path.abspath('.'), 'templates')],
            'DEBUG': False,
        }
        init_kw.update(kwargs)
        super().__init__(**init_kw)
        self._template_env = None

    @property
    def template_env(self):
        if self._template_env is None:
            from jinja2 import Environment, FileSystemLoader
            self._template_env = Environment(loader=FileSystemLoader(self['TEMPLATE_DIRS']))
        return self._template_env


def load_config_from_module(module):
    return Config(**{key: getattr(module, key)
                     for key in dir(module) if key.isupper()})


def load_config_from_pyfile(filepath):
    module = SourceFileLoader('config', filepath).load_module()
    return load_config_from_module(module)


def current_app():
    """Get your Kobin class object."""
    return request['kobin.app']


def current_config():
    """Get the configurations of your Kobin's application."""
    return current_app().config
