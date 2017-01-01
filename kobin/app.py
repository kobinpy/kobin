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
from .requests import request
from .responses import HTTPError


class Kobin:
    """
    This class is a WSGI application implementation.
    Create a instance, and run using WSGI Server.
    """
    def __init__(self, config=None):
        self.router = Router()
        self.config = config if config else load_config()
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
            response = _handle_unexpected_exception(e, self.config.get('DEBUG'))
        return response

    def __call__(self, environ, start_response):
        """It is called when receive http request."""
        response = self._handle(environ)
        start_response(response.status, response.headerlist)
        return response.body


def _get_traceback_message(e):
    message = '\n'.join(traceback.format_tb(e.__traceback__))
    return message


def _handle_unexpected_exception(e, debug):
    if debug:
        message = _get_traceback_message(e)
    else:
        message = 'Internal Server Error'
    response = HTTPError(message, 500)
    return response


# Following configurations are optional:
#
# Optional
# * DEBUG
# * SECRET_KEY
# * TEMPLATE_DIRS (default: './templates/') or TEMPLATE_ENVIRONMENT
#
def _load_jinja2_env(template_dirs, **envoptions):
    try:
        from jinja2 import Environment, FileSystemLoader
        return Environment(loader=FileSystemLoader(template_dirs), **envoptions)
    except ImportError:
        pass


def load_config(config=None):
    default_config = {
        'BASE_DIR': os.path.abspath('.'),
        'TEMPLATE_DIRS': [os.path.join(os.path.abspath('.'), 'templates')],
        'DEBUG': False,
    }
    if config is None:
        return default_config

    default_config.update(config)

    if 'TEMPLATE_ENVIRONMENT' not in config:
        env = _load_jinja2_env(default_config['TEMPLATE_DIRS'])
        if env:
            default_config['TEMPLATE_ENVIRONMENT'] = env
    return default_config


def load_config_from_module(module):
    config = {key: getattr(module, key) for key in dir(module) if key.isupper()}
    return load_config(config)


def load_config_from_pyfile(filepath):
    module = SourceFileLoader('config', filepath).load_module()
    return load_config_from_module(module)


def current_config(key, default=None):
    """Get the configurations of your Kobin's application."""
    return request['kobin.app'].config.get(key, default)
