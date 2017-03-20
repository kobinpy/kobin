from unittest import TestCase
from kobin.routes import Router
from kobin.responses import HTTPError, Response


def view_int(year: int) -> Response:
    return Response(f'hello {year}')


def view_str(name):
    return Response(f'hello {name}')


class RouterTests(TestCase):
    def test_match_dynamic_routes_with_casted_number(self):
        r = Router()
        r.add('/tests/{year}', 'GET', 'hoge', view_int)
        actual_target, actual_args = r.match('/tests/2015/', 'GET')
        self.assertEqual(actual_args, {'year': 2015})

    def test_match_dynamic_routes_with_string(self):
        r = Router()
        r.add('/tests/{name}', 'GET', 'hoge', view_str)
        actual_target, actual_args = r.match('/tests/kobin/', 'GET')
        self.assertEqual(actual_args, {'name': 'kobin'})

    def test_404_not_found(self):
        r = Router()
        r.add('/tests/{name}', 'GET', 'hoge', view_str)
        with self.assertRaises(HTTPError) as cm:
            r.match('/this_is_not_found', 'GET')
        self.assertEqual('404 Not Found', cm.exception.status)

    def test_405_method_not_allowed(self):
        r = Router()
        r.add('/tests/{name}', 'GET', 'hoge', view_str)
        with self.assertRaises(HTTPError) as cm:
            r.match('/tests/kobin', 'POST')
        self.assertEqual('405 Method Not Allowed', cm.exception.status)


class ReverseRoutingTests(TestCase):
    def setUp(self):
        self.router = Router()

        def index() -> Response:
            return Response('hello world')

        def user_detail(user_id: int) -> Response:
            return Response(f'hello user{user_id}')

        self.router.add('/', 'GET', 'top', index)
        self.router.add('/users/{user_id}', 'GET', 'user-detail', user_detail)

    def test_reverse_route_without_url_vars(self):
        actual = self.router.reverse('top')
        expected = '/'
        self.assertEqual(actual, expected)

    def test_reverse_route_with_url_vars(self):
        actual = self.router.reverse('user-detail', user_id=1)
        expected = '/users/1'
        self.assertEqual(actual, expected)

    def test_reverse_not_match(self):
        actual = self.router.reverse('foobar', foo=1)
        expected = None
        self.assertEqual(actual, expected)
