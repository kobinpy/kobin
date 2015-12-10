import re
from typing import Dict

from kobin.exceptions import HTTPError


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

    def call(self, *args):
        return self.callback(*args)


class Router(object):
    def __init__(self):
        self.routes = {}  # Search structure for static route

    def match(self, environ: Dict):
        method = environ['REQUEST_METHOD'].upper()
        path = environ['PATH_INFO'] or '/'

        if method not in self.routes:
            raise HTTPError(405, "Method Not Allowed: {}".format(method))

        for p in self.routes[method]:
            pattern = re.compile(p)
            if pattern.search(path):
                func, getargs = self.routes[method][p]
                return func, getargs(path)
        else:
            raise HTTPError(404, "Not found: {}".format(repr(path)))

    def add(self, rule: str, method: str, target: Route):
        """ Add a new rule or replace the target for an existing rule. """
        def getargs(path):
            return re.compile(rule).match(path).groups()

        self.routes.setdefault(method, {})
        self.routes[method][rule] = (target, getargs)
