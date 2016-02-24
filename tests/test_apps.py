from unittest import TestCase
from kobin import Kobin


class KobinTests(TestCase):
    def setUp(self):
        def dummy_func():
            return 'hello'

        self.app = Kobin()
        self.dummy_start_response = lambda x, y: None
        self.app.add_route('^/$', 'GET', dummy_func)

    def test_handle_view(self):
        test_env = {'REQUEST_METHOD': 'GET', 'PATH_INFO': '/'}
        actual = self.app._handle(test_env)
        expected = 'hello'
        self.assertEqual(actual, expected)

    def test_wsgi(self):
        test_env = {'REQUEST_METHOD': 'GET', 'PATH_INFO': '/'}
        actual = self.app.wsgi(test_env, self.dummy_start_response)
        expected = [b'hello']
        self.assertEqual(actual, expected)
