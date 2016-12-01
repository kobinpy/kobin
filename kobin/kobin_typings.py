from typing import Callable, Dict, List, Tuple, Union, Iterable, TypeVar
from .environs import Response, JSONResponse, TemplateResponse, HTTPError

WSGIEnvironValue = TypeVar('WSGIEnvironValue')
WSGIEnviron = Dict[str, WSGIEnvironValue]
StartResponse = Callable[[bytes, List[Tuple[str, str]]], None]

ViewResponse = Union[Response, JSONResponse, TemplateResponse, HTTPError]
WSGIResponse = Iterable[bytes]
