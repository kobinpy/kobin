from unittest import TestCase
from kobin import Kobin, Config
from . import BASE_DIR


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


class ConfigTests(TestCase):
    def setUp(self):
        self.config = Config()
        self.config.load_from_pyfile(BASE_DIR, 'dummy_config.py')

    def test_config_has_upper_case_variable(self):
        self.assertIn('UPPER_CASE', self.config)

    def test_config_has_not_lower_case_variable(self):
        self.assertNotIn('lower_case', self.config)

    def test_config_has_one_key(self):
        expected_config_len = 1
        actual = len(self.config)
        self.assertEqual(actual, expected_config_len)
