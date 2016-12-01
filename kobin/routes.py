from urllib.parse import urljoin
from typing import Callable, Dict, List, Tuple, Union, Any, get_type_hints  # type: ignore

from .environs import request, Response, HTTPError

DEFAULT_ARG_TYPE = str


def redirect(url):
    status = 303 if request.get('SERVER_PROTOCOL') == "HTTP/1.1" else 302
    return Response('', status, {'Location': urljoin(request.url, url)})


def split_by_slash(path: str) -> List[str]:
    stripped_path = path.lstrip('/').rstrip('/')
    return stripped_path.split('/')


class Route:
    """ This class wraps a route callback along with route specific metadata.
        It is also responsible for turing an URL path rule into a regular
        expression usable by the Router.
    """
    def __init__(self, rule: str, method: str, name: str,
                 callback: Union[str, bytes]) -> None:
        self.rule = rule
        self.method = method.upper()
        self.name = name
        self.callback = callback

    @property
    def callback_types(self) -> Dict[str, Any]:
        return get_type_hints(self.callback)  # type: ignore

    def get_typed_url_vars(self, url_vars: Dict[str, str]) -> Dict[str, Any]:
        typed_url_vars = {}  # type: Dict[str, Any]
        for k, v in url_vars.items():
            arg_type = self.callback_types.get(k, DEFAULT_ARG_TYPE)
            typed_url_vars[k] = arg_type(v)
        return typed_url_vars

    def _match_method(self, method: str) -> bool:
        return self.method == method.upper()

    def _match_path(self, path: str) -> Union[None, Dict[str, Any]]:
        split_rule = split_by_slash(self.rule)
        split_path = split_by_slash(path)
        url_vars = {}  # type: Dict[str, str]

        if len(split_rule) != len(split_path):
            return  # type: ignore

        for r, p in zip(split_rule, split_path):
            if r.startswith('{') and r.endswith('}'):
                url_vars[r[1:-1]] = p
                continue
            if r != p:
                return  # type: ignore
        try:
            typed_url_vars = self.get_typed_url_vars(url_vars)
        except ValueError:
            return  # type: ignore
        return typed_url_vars

    def match(self, method: str, path: str) -> Dict[str, Any]:
        if not self._match_method(method):
            return None

        url_vars = self._match_path(path)
        if url_vars is not None:
            return self.get_typed_url_vars(url_vars)


class Router:
    def __init__(self) -> None:
        self.routes = []  # type: List['Route']

    def match(self, environ: Dict[str, str]) \
            -> Tuple[Callable[..., Response], Dict[str, Any]]:
        method = environ['REQUEST_METHOD'].upper()
        path = environ['PATH_INFO'] or '/'

        for route in self.routes:
            url_vars = route.match(method, path)
            if url_vars is not None:
                return route.callback, url_vars  # type: ignore
        raise HTTPError(status=404, body='Not found: {}'.format(request.path))

    def add(self, method: str, rule: str, name: str, callback: Union[str, bytes]) -> None:
        """ Add a new rule or replace the target for an existing rule. """
        route = Route(method=method.upper(), rule=rule, name=name, callback=callback)
        self.routes.append(route)

    def reverse(self, name, **kwargs) -> str:
        for route in self.routes:
            if name == route.name:
                return route.rule.format(**kwargs)
