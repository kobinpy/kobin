import os
from unittest import TestCase
from kobin import Kobin, Config, Response


class KobinTests(TestCase):
    def setUp(self):
        self.app = Kobin()
        self.dummy_start_response = lambda x, y: None

        @self.app.route('/')
        def dummy_func():
            return Response('hello')

        @self.app.route('/test/{typed_id}')
        def typed_url_var(typed_id: int):
            body = "type: {}, value: {}".format(type(typed_id), typed_id)
            return Response(body)

        @self.app.route('/test/raise500')
        def raise500(typed_id: int):
            1 / 0
            return Response("Don't reach here")

    def test_route(self):
        test_env = {'REQUEST_METHOD': 'GET', 'PATH_INFO': '/'}
        response = self.app._handle(test_env)
        actual = response.body
        expected = [b'hello']
        self.assertEqual(actual, expected)

    def test_typed_url_var(self):
        test_env = {'REQUEST_METHOD': 'GET', 'PATH_INFO': '/test/10'}
        response = self.app._handle(test_env)
        actual = response.body
        expected = [b"type: <class 'int'>, value: 10"]
        self.assertEqual(actual, expected)

    def test_404_not_found(self):
        test_env = {'REQUEST_METHOD': 'GET', 'PATH_INFO': '/this_is_not_found'}
        response = self.app._handle(test_env)
        actual = response._status_code
        expected = 404
        self.assertEqual(actual, expected)

    def test_404_when_cast_error(self):
        test_env = {'REQUEST_METHOD': 'GET', 'PATH_INFO': '/test/not-integer'}
        response = self.app._handle(test_env)
        actual = response._status_code
        expected = 404
        self.assertEqual(actual, expected)

    def test_response_status_when_500_raised(self):
        test_env = {'REQUEST_METHOD': 'GET', 'PATH_INFO': '/test/raise500'}
        response = self.app._handle(test_env)
        actual = response._status_code
        expected = 500
        self.assertEqual(actual, expected)

    def test_response_body_when_500_raised_and_enable_debugging(self):
        self.app.config['DEBUG'] = True
        test_env = {'REQUEST_METHOD': 'GET', 'PATH_INFO': '/test/raise500'}
        response = self.app._handle(test_env)
        actual = response.body
        expected = [b'Internal Server Error']
        self.assertNotEqual(actual, expected)

    def test_response_body_when_500_raised_and_disable_debugging(self):
        test_env = {'REQUEST_METHOD': 'GET', 'PATH_INFO': '/test/raise500'}
        response = self.app._handle(test_env)
        actual = response.body
        expected = [b'Internal Server Error']
        self.assertEqual(actual, expected)

    def test_handled_body_message_when_404_not_found(self):
        test_env = {'REQUEST_METHOD': 'GET', 'PATH_INFO': '/this_is_not_found'}
        response = self.app._handle(test_env)
        actual = response.body
        expected = [b"Not found: /this_is_not_found"]
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
