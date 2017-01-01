"""
Routing
=======

Kobin's routing system may be slightly distinctive.

Rule Syntax
-----------

Kobin use decorator based URL dispatch.

* Dynamic convert URL variables from Type Hints.

.. code-block:: python

   from kobin import Kobin, Response, RedirectResponse
   app = Kobin()

   @app.route('/')
   def index() -> Response:
       return Response('Hello World')

   @app.route('/users/{user_id}')
   def index(user_id: str) -> Response:
       return Response('User List')


Reverse Routing
---------------

`app.router.reverse` function returns URL.
The usage is like this:

.. code-block:: python

   from kobin import Kobin, Response
   app = Kobin()

   @app.route('/', 'top-page')
   def index() -> Response:
       return Response('Hello World')

   @app.route('/users/{user_id}', 'user-detail')
   def user_detail(user_id: int) -> Response:
       return Response('Hello User{}'.format(user_id))

   print(app.router.reverse('top-page'))
   # http://hostname/

   print(app.router.reverse('user-detail', user_id=1))
   # http://hostname/users/1


Reverse Routing and Redirecting
-------------------------------

:class:`RedirectResponse`
The usage is like this:

.. code-block:: python

   from kobin import Kobin, Response, RedirectResponse
   app = Kobin()

   @app.route('/', 'top-page')
   def index() -> Response:
       return Response('Hello World')

   @app.route('/404')
   def user_detail() -> Response:
       top_url = app.router.reverse('top-page')
       return RedirectResponse(top_url)

"""
from typing import get_type_hints
from .requests import request
from .responses import HTTPError

DEFAULT_ARG_TYPE = str


def split_by_slash(path):
    stripped_path = path.lstrip('/').rstrip('/')
    return stripped_path.split('/')


class Route:
    def __init__(self, rule, method, name, callback):
        self.rule = rule
        self.method = method.upper()
        self.name = name
        self.callback = callback

    @property
    def callback_types(self):
        return get_type_hints(self.callback)

    def get_typed_url_vars(self, url_vars):
        typed_url_vars = {}
        for k, v in url_vars.items():
            arg_type = self.callback_types.get(k, DEFAULT_ARG_TYPE)
            typed_url_vars[k] = arg_type(v)
        return typed_url_vars

    def _match_method(self, method):
        return self.method == method.upper()

    def _match_path(self, path):
        split_rule = split_by_slash(self.rule)
        split_path = split_by_slash(path)
        url_vars = {}

        if len(split_rule) != len(split_path):
            return

        for r, p in zip(split_rule, split_path):
            if r.startswith('{') and r.endswith('}'):
                url_vars[r[1:-1]] = p
                continue
            if r != p:
                return
        try:
            typed_url_vars = self.get_typed_url_vars(url_vars)
        except ValueError:
            return
        return typed_url_vars

    def match(self, method, path):
        if not self._match_method(method):
            return None

        url_vars = self._match_path(path)
        if url_vars is not None:
            return self.get_typed_url_vars(url_vars)


class Router:
    def __init__(self) -> None:
        self.routes = []

    def match(self, environ):
        method = environ['REQUEST_METHOD'].upper()
        path = environ['PATH_INFO'] or '/'

        for route in self.routes:
            url_vars = route.match(method, path)
            if url_vars is not None:
                return route.callback, url_vars
        raise HTTPError(status=404, body='Not found: {}'.format(request.path))

    def add(self, method, rule, name, callback):
        """ Add a new rule or replace the target for an existing rule. """
        route = Route(method=method.upper(), rule=rule, name=name, callback=callback)
        self.routes.append(route)

    def reverse(self, name, **kwargs):
        for route in self.routes:
            if name == route.name:
                return route.rule.format(**kwargs)
