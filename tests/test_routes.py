from unittest import TestCase
from kobin.routes import Route, Router, type_args
from kobin.exceptions import HTTPError
import sys


class TypeArgsTests(TestCase):
    def test_type_args(self):
        input_type_hints = {'id': int, 'return': None}
        input_args_dict = {'id': '1'}
        actual = type_args(input_args_dict, input_type_hints)
        self.assertEqual(actual['id'], 1)

    def test_default_type(self):
        input_type_hints = {'return': None}
        input_args_dict = {'id': '1'}
        actual = type_args(input_args_dict, input_type_hints)
        self.assertEqual(actual['id'], '1')


class RouteTests(TestCase):
    def test_call(self):
        def dummy_func(num: int) -> None:
            return num
        route = Route('/hoge', 'GET', dummy_func)
        self.assertEqual(route.call(**{'num': 1}), 1)


class RouterTests(TestCase):
    def setUp(self):
        self.router = Router()

    def test_match_static_routes(self):
        def dummy_func() -> None:
            pass
        route = Route('/user/(?P<num>\d+', 'GET', dummy_func)

        self.router.add('^/tests/$', 'GET', route)
        test_env = {'REQUEST_METHOD': 'GET', 'PATH_INFO': '/tests/'}
        actual_target, actual_args = self.router.match(test_env)

        self.assertIsNone(actual_args)

    def test_match_dynamic_routes_with_casted_number(self):
        def dummy_func(year: int) -> None:
            return year
        route = Route('/years/(?P<year>\d{4}', 'GET', dummy_func)

        self.router.add('^/tests/(?P<year>\d{4})/$', 'GET', route)
        test_env = {'REQUEST_METHOD': 'GET', 'PATH_INFO': '/tests/2015/'}
        actual_target, actual_args = self.router.match(test_env)
        self.assertEqual(actual_args, {'year': 2015})

    def test_match_dynamic_routes_with_string(self):
        def dummy_func(name):
            return name
        route = Route('^/tests/(?P<name>\w+)/$', 'GET', dummy_func)

        self.router.add(route.rule, route.method, route)
        test_env = {'REQUEST_METHOD': 'GET', 'PATH_INFO': '/tests/kobin/'}
        actual_target, actual_args = self.router.match(test_env)
        self.assertEqual(actual_args, {'name': 'kobin'})

    def test_404_not_found(self):
        def dummy_func(name):
            return name
        route = Route('^/tests/(?P<name>\w+)/$', 'GET', dummy_func)

        self.router.add(route.rule, route.method, route)
        test_env = {'REQUEST_METHOD': 'GET', 'PATH_INFO': '/this_is_not_found'}
        self.assertRaises(HTTPError, self.router.match, test_env)
