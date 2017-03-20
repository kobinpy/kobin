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
from .responses import HTTPError


def split_by_slash(path):
    stripped_path = path.lstrip('/').rstrip('/')
    return stripped_path.split('/')


def match_url_vars_type(url_vars, type_hints):
    """ Match types of url vars.

    >>> match_url_vars_type({'user_id': '1'}, {'user_id': int})
    True, {'user_id': 1}
    >>> match_url_vars_type({'user_id': 'foo'}, {'user_id': int})
    False, {}
    """
    typed_url_vars = {}
    try:
        for k, v in url_vars.items():
            arg_type = type_hints.get(k)
            if arg_type and arg_type != str:
                typed_url_vars[k] = arg_type(v)
            else:
                typed_url_vars[k] = v
    except ValueError:
        return False, {}
    return True, typed_url_vars


def match_path(rule, path):
    """ Match path.

    >>> match_path('/foo', '/foo')
    True, {}
    >>> match_path('/foo', '/bar')
    False, {}
    >>> match_path('/users/{user_id}', '/users/1')
    True, {'user_id', 1}
    >>> match_path('/users/{user_id}', '/users/not-integer')
    True, {'user_id': 'not-integer'}
    """
    split_rule = split_by_slash(rule)
    split_path = split_by_slash(path)
    url_vars = {}

    if len(split_rule) != len(split_path):
        return False, {}

    for r, p in zip(split_rule, split_path):
        if r.startswith('{') and r.endswith('}'):
            url_vars[r[1:-1]] = p
            continue
        if r != p:
            return False, {}
    return True, url_vars


class Router:
    def __init__(self) -> None:
        self.endpoints = []

    def match(self, path, method):
        """ Get callback and url_vars.

        >>> from kobin import Response
        >>> r = Router()
        >>> def view(user_id: int) -> Response:
        ...     return Response(f'You are {user_id}')
        ...
        >>> r.add('/users/{user_id}', 'GET', 'user-detail', view)

        >>> callback, url_vars = r.match('/users/1', 'GET')
        >>> url_vars
        {'user_id': 1}
        >>> callback(**url_vars)
        You are 1

        >>> callback, url_vars = r.match('/notfound', 'GET')
        >>> callback(**url_vars)
        404 Not Found
        """
        if path != '/':
            path = path.rstrip('/')
        method = method.upper()

        status = 404
        for p, n, m in self.endpoints:
            matched, url_vars = match_path(p, path)
            if not matched:  # path: not matched
                continue

            if method not in m:  # path: matched, method: not matched
                status = 405
                raise HTTPError(status=status, body=f'Method not found: {path} {method}')  # it has security issue??

            callback, type_hints = m[method]
            type_matched, typed_url_vars = match_url_vars_type(url_vars, type_hints)
            if not type_matched:
                continue  # path: not matched (types are different)
            return callback, typed_url_vars
        raise HTTPError(status=status, body=f'Not found: {path}')

    def add(self, rule, method, name, callback):
        """ Add a new rule or replace the target for an existing rule.

        >>> from kobin import Response
        >>> r = Router()
        >>> def view(user_id: int) -> Response:
        ...     return Response(f'You are {user_id}')
        ...
        >>> r.add('/users/{user_id}', 'GET', 'user-detail', view)
        >>> r.endpoints[0]
        ('/users/{user_id}', 'user-detail', {'GET': (view, {'user_id': int})})
        """
        if rule != '/':
            rule = rule.rstrip('/')
        method = method.upper()

        for i, e in enumerate(self.endpoints):
            r, n, callbacks = e
            if r == rule:
                assert name == n and n is not None, (
                    "A same path should set a same name for reverse routing."
                )
                callbacks[method] = (callback, get_type_hints(callback))
                self.endpoints[i] = (r, name, callbacks)
                break
        else:
            e = (rule, name, {method: (callback, get_type_hints(callback))})
            self.endpoints.append(e)

    def reverse(self, name, **kwargs):
        """ Reverse routing.

        >>> from kobin import Response
        >>> r = Router()
        >>> def view(user_id: int) -> Response:
        ...     return Response(f'You are {user_id}')
        ...
        >>> r.add('/users/{user_id}', 'GET', 'user-detail', view)
        >>> r.reverse('user-detail', user_id=1)
        '/users/1'
        """
        for p, n, _ in self.endpoints:
            if name == n:
                return p.format(**kwargs)
