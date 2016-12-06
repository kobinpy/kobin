from typing import Callable, Dict, List, Tuple, Union, Iterable, TypeVar
from types import ModuleType

from .routes import Router
from .environs import Response, JSONResponse, TemplateResponse, HTTPError


WSGIEnvironValue = TypeVar('WSGIEnvironValue')
WSGIEnviron = Dict[str, WSGIEnvironValue]
StartResponse = Callable[[bytes, List[Tuple[str, str]]], None]

ViewResponse = Union[Response, JSONResponse, TemplateResponse, HTTPError]
ViewFunction = Callable[..., ViewResponse]
WSGIResponse = Iterable[bytes]


class Kobin:
    router: Router
    config: Config
    before_request_callback: Callable[[], None]
    after_request_callback: Callable[[Response], Response]

    def __init__(self, root_path: str = ...) -> None: ...
    def route(self, rule: str = ..., method: str = ..., name: str = ...,
              callback: ViewFunction = ...) -> ViewFunction: ...
    def before_request(self, callback: Callable[[], None]) -> Callable[[], None]: ...
    def after_request(self, callback: Callable[[Response], Response]) -> \
            Callable[[Response], Response]: ...
    def _handle(self, environ: WSGIEnviron) -> ViewResponse: ...
    def wsgi(self, environ: WSGIEnviron, start_response: StartResponse) -> WSGIResponse: ...
    def __call__(self, environ: WSGIEnviron, start_response: StartResponse) -> WSGIResponse: ...


class Config(dict):
    root_path: str
    default_config: WSGIEnviron

    def __init__(self, root_path: str, *args: str, **kwargs: WSGIEnvironValue) -> None: ...
    def load_from_pyfile(self, file_name: str) -> None: ...
    def load_from_module(self, module: ModuleType) -> None: ...
    def update_jinja2_environment(self) -> None: ...


def current_app() -> Kobin: ...
def current_config() -> Config: ...
