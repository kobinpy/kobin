from datetime import timedelta, date, datetime
from http.cookies import SimpleCookie
from typing import Dict, List, Tuple, Any, Iterable, Callable, Union
from wsgiref.headers import Headers  # type: ignore

WSGIEnviron = Dict[str, Any]


HTTP_CODES: Dict[int, str]
_HTTP_STATUS_LINES: Dict[int, str]


class BaseResponse:
    default_status: int
    default_content_type: str
    headers: Headers
    _body: bytes
    _status_code: int
    _cookies: SimpleCookie

    def __init__(self, body: Iterable[bytes] = ..., status: int = ..., headers: Dict = ...) -> None: ...
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
    def set_cookie(self, key: str, value: str,
                   expires: Union[date, datetime, int] = ..., max_age: Union[timedelta, int] = ...,
                   path: str = ..., secret: Union[str, bytes] = ...,
                   digestmod: Callable[..., bytes] = ...) -> None: ...
    def delete_cookie(self, key: str, **kwargs: Any) -> None: ...

class Response:
    def __init__(self, body: Union[str, bytes] = ..., status: int = ..., headers: Dict = ...,
                 charset: str = ...) -> None: ...

class JSONResponse:
    def __init__(self, dic: Dict, status: int = ..., headers: Dict = ...,
                 charset: str = ..., **dump_args: Any) -> None: ...


class TemplateResponse:
    def __init__(self, filename: str, status: int = ..., headers: Dict[str, str] = ...,
                 charset: str = ..., **tpl_args: Any) -> None: ...


class RedirectResponse(Response):
    def __init__(self, url: str) -> None:
        super().__init__()
        ...


class HTTPError(Response, Exception):
    default_status: int

    def __init__(self, body: str, status: int = ..., headers: Dict = ...,
                 charset: str = ...) -> None: ...
