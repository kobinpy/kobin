from typing import Dict
from kobin.exceptions import HTTPError


class Router(object):
    def __init__(self):
        self.static = {}  # Search structure for static route
        self.builder = {}  # Data structure for the url builder

    def match(self, environ: Dict):
        method = environ['REQUEST_METHOD'].upper()
        path = environ['PATH_INFO'] or '/'

        if method in self.static and path in self.static[method]:
            target, getargs = self.static[method][path]
            return target, getargs(path) if getargs else {}
        raise HTTPError(404, "Not found: " + repr(path))

    def _split_routes(self, rules: str):
        return [rule for rule in rules.split('/') if rule]

    def add(self, rule: str, method: str, target: Route):
        """ Add a new rule or replace the target for an existing rule. """
        self.static.setdefault(method, {})
        self.static[method][rule] = (target, None)  # the static root doesn't have args


class Route(object):
    """ This class wraps a route callback along with route specific metadata.
        It is also responsible for turing an URL path rule into a regular
        expression usable by the Router.
    """
    def __init__(self, app, rule: str, method: str, callback):
        self.app = app
        self.rule = rule
        self.method = method
        self.callback = callback

    def call(self):
        return self.callback()
