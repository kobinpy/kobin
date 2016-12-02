from jinja2 import Template  # type: ignore
from http.cookies import SimpleCookie
from typing import Dict, List, Tuple, Any, Iterable, TypeVar, Callable
from wsgiref.headers import Headers  # type: ignore

WSGIEnvironValue = TypeVar('WSGIEnvironValue')
WSGIEnviron = Dict[str, WSGIEnvironValue]


class Request:
    __slots__ = ... # type: List[str]
    environ = ... # type: WSGIEnviron
    _body = ... # type: str

    def __init__(self, environ: Dict = ...) -> None: ...
    def get(self, value: str, default: Any = ...): ...
    @property
    def path(self) -> str: ...
    @property
    def method(self) -> str: ...
    @property
    def GET(self) -> Dict[str, str]: ...
    @property
    def POST(self) -> Dict[str, str]: ...
    @property
    def body(self) -> str: ...
    @property
    def json(self) -> Dict[str, Any]: ...
    @property
    def url(self) -> str: ...
    @property
    def cookies(self) -> Dict[str, str]: ...
    def get_cookie(self, key: str, default: str = ..., secret: str = ...) -> str: ...
    def __getitem__(self, key: str): ...
    def __delitem__(self, key: str): ...
    def __setitem__(self, key: str, value: Any): ...
    def __len__(self): ...
    def __repr__(self): ...


def _local_property() -> Any: ...


class LocalRequest(Request):
    bind = ...  # type: Callable[[Dict], None]
    environ = ...  # type: WSGIEnviron
    _body = ...  # type: str


request = ...  # type: LocalRequest

HTTP_CODES = ... # type: Dict[int, str]
_HTTP_STATUS_LINES = ... # type: Dict[int, str]


class Response:
    default_status = ...  # type: int
    default_content_type = ...  # type: str
    headers = ... # type: Headers
    _body = ... # type: str
    _status_code = ... # type: int
    _cookies = ... # type: SimpleCookie
    charset = ... # type: str

    def __init__(self, body: str = ..., status: int = ..., headers: Dict = ...,
                 charset: str = ...) -> None: ...
    @property
    def body(self) -> Iterable[bytes]: ...
    @property
    def status_code(self) -> int: ...
    @property
    def status(self) -> str: ...
    @status.setter
    def status(self, status_code: int) -> None: ...
    @property
    def headerlist(self) -> List[Tuple[str, str]]: ...
    def set_cookie(self, key: str, value: Any, expires: str = ..., path: str = ...,
                   **options: Any) -> None: ...
    def delete_cookie(self, key: str, **kwargs: Any) -> None: ...

class JSONResponse(Response):
    dic = ... # type: Dict[str, Any]
    json_dump_args = ... # type: Dict[str, Any]

    def __init__(self, dic: Dict, status: int = ..., headers: Dict = ...,
                 charset: str = ..., **dump_args: Any) -> None: ...
    @property
    def body(self) -> Iterable[bytes]: ...


class TemplateResponse(Response):
    template = ... # type: Template
    tpl_args = ... # type: Dict[str, Any]

    def __init__(self, filename: str, status: int = ..., headers: Dict[str, str] = ...,
                 charset: str = ..., **tpl_args: Any) -> None: ...
    @property
    def body(self) -> Iterable[bytes]: ...


class RedirectResponse(Response):
    def __init__(self, url: str) -> None: ...


class HTTPError(Response, Exception):
    def __init__(self, body: str, status: int = ..., headers: Dict = ...,
                 charset: str = ...) -> None: ...
