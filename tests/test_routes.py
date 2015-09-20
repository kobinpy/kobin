from unittest import TestCase
from kobin.routes import Router


class RouterTest(TestCase):
    def setUp(self):
        self.router = Router()

    def test_split_routes(self):
        input_route = '/user/mypage'
        expected_route = ['user', 'mypage']
        actual_route = self.router._split_routes(input_route)
        self.assertListEqual(actual_route, expected_route)

    def test_add_func_when_input_static(self):
        def target_func(): pass
        self.router.add('/user/', 'GET', target_func)

        actual = self.router.static
        self.assertIn('GET', actual)
        self.assertIn('/user/', actual['GET'])
        expected_tuple = (target_func, None)
        self.assertTupleEqual(actual['GET']['/user/'], expected_tuple)
