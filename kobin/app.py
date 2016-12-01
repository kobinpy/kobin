from importlib.machinery import SourceFileLoader  # type: ignore
from jinja2 import Environment, FileSystemLoader  # type: ignore
import os
import traceback
from typing import Any, Callable, Dict

from .routes import Router
from .environs import request, Response, HTTPError
from .kobin_typings import (
    WSGIEnviron, WSGIEnvironValue, WSGIResponse, StartResponse,
    ViewResponse
)


class Kobin:
    def __init__(self, root_path: str='.') -> None:
        self.router = Router()
        self.config = Config(os.path.abspath(root_path))

    def route(self, rule: str=None, method: str='GET', name: str=None,
              callback: Callable[..., ViewResponse]=None) -> Callable[..., ViewResponse]:
        def decorator(callback_func: Callable[..., Response]) -> Callable[..., ViewResponse]:
            self.router.add(method, rule, name, callback_func)
            return callback_func
        return decorator(callback) if callback else decorator

    def _handle(self, environ: WSGIEnviron) -> ViewResponse:
        environ['kobin.app'] = self
        request.bind(environ)  # type: ignore

        try:
            callback, kwargs = self.router.match(environ)
            response = callback(**kwargs) if kwargs else callback()
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

    def wsgi(self, environ: WSGIEnviron, start_response: StartResponse) -> WSGIResponse:
        response = self._handle(environ)
        start_response(response.status, response.headerlist)
        return response.body

    def __call__(self, environ: WSGIEnviron, start_response: StartResponse) -> WSGIResponse:
        """It is called when receive http request."""
        return self.wsgi(environ, start_response)


class Config(dict):
    default_config = {  # type: WSGIEnviron
        'BASE_DIR': os.path.abspath('.'),
        'TEMPLATE_DIRS': [os.path.join(os.path.abspath('.'), 'templates')],
        'DEBUG': False,
    }

    def __init__(self, root_path: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.root_path = root_path
        self.update(self.default_config)
        self.update_jinja2_environment()

    def load_from_pyfile(self, file_name: str) -> None:
        file_path = os.path.join(self.root_path, file_name)
        module = SourceFileLoader('config', file_path).load_module()  # type: ignore
        self.load_from_module(module)

    def load_from_module(self, module) -> None:
        configs = {key: getattr(module, key) for key in dir(module) if key.isupper()}
        self.update(configs)
        self.update_jinja2_environment()

    def update_jinja2_environment(self) -> None:
        self['JINJA2_ENV'] = Environment(loader=FileSystemLoader(self['TEMPLATE_DIRS']))


def current_app() -> Kobin:
    return request['kobin.app']


def current_config() -> Config:
    return current_app().config
