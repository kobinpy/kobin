import os
from unittest import TestCase
from kobin import Kobin, Config, current_app, current_config


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
        test_env = {'REQUEST_METHOD': 'GET', 'PATH_INFO': '/10'}
        actual = self.app._handle(test_env)
        expected = 10
        self.assertEqual(actual, expected)

    def test_wsgi(self):
        test_env = {'REQUEST_METHOD': 'GET', 'PATH_INFO': '/'}
        actual = self.app.wsgi(test_env, self.dummy_start_response)
        expected = [b'hello']
        self.assertEqual(actual, expected)


class ConfigTests(TestCase):
    def setUp(self):
        self.root_path = os.path.dirname(os.path.abspath(__file__))

    def test_constructor_set_root_path(self):
        config = Config(self.root_path)
        config.load_from_pyfile('dummy_config.py')
        self.assertIn('root_path', dir(config))

    def test_load_from_module(self):
        from tests import dummy_config
        config = Config(self.root_path)
        config.load_from_module(dummy_config)
        self.assertIn('UPPER_CASE', config)

    def test_load_from_pyfile(self):
        config = Config(self.root_path)
        config.load_from_pyfile('dummy_config.py')
        self.assertIn('UPPER_CASE', config)

    def test_config_has_not_lower_case_variable(self):
        config = Config(self.root_path)
        config.load_from_pyfile('dummy_config.py')
        self.assertNotIn('lower_case', config)

    def test_failure_for_loading_config(self):
        config = Config(self.root_path)
        self.assertRaises(FileNotFoundError, config.load_from_pyfile, 'no_exists.py')
