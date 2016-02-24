from unittest import TestCase
from kobin import Kobin


class KobinTests(TestCase):
    def setUp(self):
        self.app = Kobin()
        self.dummy_start_response = lambda x, y: None

        @self.app.route('^/$')
        def dummy_func():
            return 'hello'

        @self.app.route('^/(?P<typed_id>\d+)$')
        def typed_url_var(typed_id: int):
            return typed_id

    def test_route(self):
        test_env = {'REQUEST_METHOD': 'GET', 'PATH_INFO': '/'}
        actual = self.app._handle(test_env)
        expected = 'hello'
        self.assertEqual(actual, expected)

    def test_typed_url_var(self):
        test_env = {'REQUEST_METHOD': 'GET', 'PATH_INFO': '/3'}
        actual = self.app._handle(test_env)
        expected = 3
        self.assertEqual(actual, expected)

    def test_wsgi(self):
        test_env = {'REQUEST_METHOD': 'GET', 'PATH_INFO': '/'}
        actual = self.app.wsgi(test_env, self.dummy_start_response)
        expected = [b'hello']
        self.assertEqual(actual, expected)
