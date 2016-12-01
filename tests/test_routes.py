from unittest import TestCase
from kobin.routes import Route, Router
from kobin.environs import HTTPError


class RouteTests(TestCase):
    def test_call(self):
        def dummy_func(num: int):
            return num
        route = Route('/hoge/{num}', 'GET', 'hoge', dummy_func)
        self.assertEqual(route.callback(**{'num': 1}), 1)

    def test_match_method(self):
        def dummy_func(num: int):
            return num
        route = Route('/hoge/{num}', 'GET', 'hoge', dummy_func)
        self.assertTrue(route._match_method('GET'))

    def test_match_path(self):
        def dummy_func(num: int):
            return num
        route = Route('/hoge/{num}', 'GET', 'hoge', dummy_func)
        self.assertTrue(route._match_path('/hoge/1'))

    def test_match_path_with_slash(self):
        def dummy_func(num: int):
            return num
        route = Route('/hoge/{num}', 'GET', 'hoge', dummy_func)
        self.assertTrue(route._match_path('hoge/1/'))

    def test_match(self):
        def dummy_func(num: int):
            return num
        route = Route('/hoge/{num}', 'GET', 'hoge', dummy_func)
        self.assertTrue(route.match('GET', 'hoge/1/'))


class RouterTests(TestCase):
    def setUp(self):
        self.router = Router()

    def test_match_dynamic_routes_with_casted_number(self):
        def dummy_func(year: int) -> int:
            return year

        self.router.add('GET', '/tests/{year}', 'hoge', dummy_func)
        test_env = {'REQUEST_METHOD': 'GET', 'PATH_INFO': '/tests/2015/'}
        actual_target, actual_args = self.router.match(test_env)
        self.assertEqual(actual_args, {'year': 2015})

    def test_match_dynamic_routes_with_string(self):
        def dummy_func(name):
            return name

        self.router.add('GET', '/tests/{name}', 'hoge', dummy_func)
        test_env = {'REQUEST_METHOD': 'GET', 'PATH_INFO': '/tests/kobin/'}
        actual_target, actual_args = self.router.match(test_env)
        self.assertEqual(actual_args, {'name': 'kobin'})

    def test_404_not_found(self):
        def dummy_func(name):
            return name

        self.router.add('GET', '/tests/{name}', 'hoge', dummy_func)
        test_env = {'REQUEST_METHOD': 'GET', 'PATH_INFO': '/this_is_not_found'}
        self.assertRaises(HTTPError, self.router.match, test_env)
