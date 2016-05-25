import os
from unittest import TestCase
from unittest.mock import patch

from kobin.static_files import static_file
from kobin import Kobin, response
from kobin.exceptions import HTTPError


class StaticFileViewTests(TestCase):
    def setUp(self):
        self.app = Kobin()
        self.app.config.update({
            'STATIC_ROOT': '/static/',
            'STATICFILES_DIRS': [os.path.join(os.path.dirname(os.path.abspath(__name__)), 'static')]
        })

    def test_routing_to_static_file(self):
        test_env = {'REQUEST_METHOD': 'GET', 'PATH_INFO': '/static/static.css'}
        actual_target, _ = self.app.router.match(test_env)
        self.assertEqual(actual_target.callback, static_file)

    def test_urlvars(self):
        test_env = {'REQUEST_METHOD': 'GET', 'PATH_INFO': '/static/static.css'}
        _, url_vars = self.app.router.match(test_env)
        actual_filename = url_vars['filename']
        self.assertEqual(actual_filename, 'static.css')


class StaticFilesTests(TestCase):
    dummy_current_config = {
        'STATIC_ROOT': '/static/',
        'STATICFILES_DIRS': [os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')]
    }

    @patch('kobin.app.current_config')
    def test_return_static_file(self, mock_current_config):
        mock_current_config.return_value = self.dummy_current_config
        actual = static_file('static.css')
        expected = 'body { color: black; }\n'.encode('utf-8')
        self.assertEqual(actual, expected)

    @patch('kobin.app.current_config')
    def test_static_file_404_not_found(self, mock_current_config):
        mock_current_config.return_value = self.dummy_current_config
        self.assertRaises(HTTPError, static_file, 'not_found.png')

    @patch('kobin.app.current_config')
    def test_exist_last_modified_in_headers(self, mock_current_config):
        mock_current_config.return_value = self.dummy_current_config
        static_file('static.css')
        self.assertIn('Last-Modified', response._headers)

    @patch('kobin.app.current_config')
    def test_content_length(self, mock_current_config):
        mock_current_config.return_value = self.dummy_current_config
        expected_content_length = str(23)
        static_file('static.css')
        actual_content_length = response._headers['Content-Length']
        self.assertIn(expected_content_length, actual_content_length)

    @patch('kobin.app.current_config')
    def test_content_type(self, mock_current_config):
        mock_current_config.return_value = self.dummy_current_config
        expected_content_type = 'text/css; charset=UTF-8'
        static_file('static.css')
        actual_content_type = response._headers['Content-Type']
        self.assertIn(expected_content_type, actual_content_type)
