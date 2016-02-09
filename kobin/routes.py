import re
from typing import Callable, Dict, List, Any, get_type_hints  # type: ignore

from kobin.exceptions import HTTPError

DEFAULT_ARG_TYPE = str


def type_args(args_dict: Dict[str, str], type_hints: Dict[str, Any]) -> Dict[str, Any]:
    for k, v in args_dict.items():
        arg_type = type_hints.get(k, DEFAULT_ARG_TYPE)
        args_dict[k] = arg_type(v)
        return args_dict


class Route(object):
    """ This class wraps a route callback along with route specific metadata.
        It is also responsible for turing an URL path rule into a regular
        expression usable by the Router.
    """
    def __init__(self, rule: str, method: str, callback: Callable[..., str]) -> None:
        self.rule = rule
        self.method = method
        self.callback = callback
        self.callback_types = get_type_hints(callback)  # type: Dict[str, Any]

    def call(self, **kwargs):
        return self.callback(**kwargs)


class Router(object):
    def __init__(self) -> None:
        # Search structure for static route
        self.routes = {}  # type: Dict[str, Dict[str, List[Any]]]

    def match(self, environ: Dict[str, str]):
        method = environ['REQUEST_METHOD'].upper()
        path = environ['PATH_INFO'] or '/'

        if method not in self.routes:
            raise HTTPError(405, "Method Not Allowed: {}".format(method))

        for p in self.routes[method]:
            pattern = re.compile(p)
            if pattern.search(path):
                route, getargs = self.routes[method][p]
                return route, getargs(path)
        else:
            raise HTTPError(404, "Not found: {}".format(repr(path)))

    def add(self, rule: str, method: str, route: Route) -> None:
        """ Add a new rule or replace the target for an existing rule. """
        def getargs(path: str) -> Dict[str, Any]:
            args_dict = re.compile(rule).match(path).groupdict()
            return type_args(args_dict, route.callback_types)

        self.routes.setdefault(method, {})
        self.routes[method][rule] = (route, getargs)  # type: ignore
