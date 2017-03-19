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
import logging
import os
import traceback
from urllib.parse import urljoin
import warnings

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
        self.config = load_config(config)
        self.before_request_callbacks = []
        self.after_request_callbacks = []
        self.logger = self.config.get('LOGGER')
        self._frozen = False

    def __setattr__(self, *args, **kwargs):
        if '_frozen' in dir(self):
            if self._frozen:
                warnings.warn("Cannot Change the state of started application!",
                              stacklevel=2)
        else:
            super().__setattr__(*args, **kwargs)

    def route(self, rule=None, method='GET', name=None, callback=None):
        def decorator(callback_func):
            self.router.add(method, rule, name, callback_func)
            return callback_func
        return decorator(callback) if callback else decorator

    def before_request(self, callback):
        def decorator(callback_func):
            self.before_request_callbacks.append(callback_func)
            return callback_func
        return decorator(callback)

    def after_request(self, callback):
        def decorator(callback_func):
            self.after_request_callbacks.append(callback_func)
            return callback_func
        return decorator(callback)

    def _handle(self, environ):
        environ['kobin.app'] = self
        request.bind(environ)

        try:
            for before_request_callback in self.before_request_callbacks:
                before_request_callback()

            callback, kwargs = self.router.match(environ)
            response = callback(**kwargs) if kwargs else callback()

            for after_request_callback in self.after_request_callbacks:
                wrapped_response = after_request_callback(response)
                if wrapped_response:
                    response = wrapped_response
        except HTTPError as e:
            response = e
        except BaseException as e:
            error_message = _get_exception_message(e, self.config.get('DEBUG'))
            self.logger.debug(error_message)
            response = HTTPError(error_message, 500)
        return response

    def __call__(self, environ, start_response):
        """It is called when receive http request."""
        if not self._frozen:
            self._frozen = True
        response = self._handle(environ)
        start_response(response.status, response.headerlist)
        return response.body


def _get_exception_message(e, debug):
    if debug:
        stacktrace = '\n'.join(traceback.format_tb(e.__traceback__))
        message = f"500: Internal Server Error\n\n" \
                  f"Exception:\n  {repr(e)}\n\n" \
                  f"Stacktrace:\n{stacktrace}\n"
    else:
        message = 'Internal Server Error'
    return message


# Following configurations are optional:
#
# * DEBUG
# * SECRET_KEY
# * TEMPLATE_DIRS (default: './templates/') or TEMPLATE_ENVIRONMENT
# * LOG_LEVEL
# * LOG_HANDLER
#
def _current_app():
    # This function exists for unittest.mock.patch.
    return request['kobin.app']


def template_router_reverse(name, with_host=False):
    url = _current_app().router.reverse(name)
    if with_host:
        url = urljoin(request.url, url)

    if url is None:
        return ''
    return url


def load_jinja2_env(template_dirs,  global_variables=None, global_filters=None, **envoptions):
    try:
        from jinja2 import Environment, FileSystemLoader
        env = Environment(loader=FileSystemLoader(template_dirs), **envoptions)
        if global_variables:
            env.globals.update(global_variables)
        if global_filters:
            env.filters.update(global_filters)
        return env
    except ImportError:
        pass


def _get_default_logger(debug):
    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler()
    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    return logger


def load_config(config=None):
    default_config = {
        'BASE_DIR': os.path.abspath('.'),
        'TEMPLATE_DIRS': [os.path.join(os.path.abspath('.'), 'templates')],
        'DEBUG': False,
    }
    if config is not None:
        default_config.update(config)

    if 'TEMPLATE_ENVIRONMENT' not in default_config:
        env = load_jinja2_env(default_config['TEMPLATE_DIRS'])
        if env:
            default_config['TEMPLATE_ENVIRONMENT'] = env

    if 'LOGGER' not in default_config:
        default_config['LOGGER'] = _get_default_logger(default_config.get('DEBUG'))

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
