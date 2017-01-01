import os
from unittest import TestCase
from unittest.mock import patch

from kobin import Kobin, load_config
from kobin.responses import (
    BaseResponse, Response, JSONResponse, TemplateResponse, RedirectResponse,
)

TEMPLATE_DIRS = [os.path.join(os.path.dirname(__file__), 'templates')]


class BaseResponseTests(TestCase):
    def test_constructor_body(self):
        response = BaseResponse([b'Body'])
        self.assertEqual([b'Body'], response.body)

    def test_constructor_status(self):
        response = BaseResponse([b'Body'], 200)
        self.assertEqual(response.status_code, 200)

    def test_set_status(self):
        response = BaseResponse()
        response.status = 200
        self.assertEqual(response.status, '200 OK')

    def test_set_invalid_status(self):
        response = BaseResponse()

        def set_status(status):
            response.status = status

        self.assertRaises(ValueError, set_status, -1)

    def test_constructor_headerlist(self):
        response = BaseResponse()
        expected_content_type = ('Content-Type', 'text/plain;')
        self.assertIn(expected_content_type, response.headerlist)

    def test_constructor_headerlist_has_already_content_type(self):
        response = BaseResponse()
        response.headers.add_header('Content-Type', 'application/json')
        expected_content_type = ('Content-Type', 'application/json')
        self.assertIn(expected_content_type, response.headerlist)
        expected_content_type = ('Content-Type', 'text/html; charset=UTF-8')
        self.assertNotIn(expected_content_type, response.headerlist)

    def test_add_header(self):
        response = BaseResponse()
        response.headers.add_header('key', 'value')
        self.assertIn(('key', 'value'), response.headerlist)

    def test_constructor_headerlist_with_add_header(self):
        response = BaseResponse(headers={'key1': 'value1'})
        expected_content_type = ('key1', 'value1')
        self.assertIn(expected_content_type, response.headerlist)


class ResponseTests(TestCase):
    def test_constructor_status(self):
        response = Response('Body', charset='utf-8')
        self.assertEqual(response.status_code, 200)

    def test_constructor_body_when_given_bytes(self):
        response = Response(b'Body')
        self.assertEqual([b'Body'], response.body)

    def test_constructor_body_when_given_str(self):
        response = Response('Body')
        self.assertEqual([b'Body'], response.body)


class JSONResponseTests(TestCase):
    def test_constructor_status(self):
        response = JSONResponse({'foo': 'bar'})
        self.assertEqual(response.status_code, 200)

    def test_constructor_headerlist(self):
        response = JSONResponse({'foo': 'bar'})
        expected_content_type = ('Content-Type', 'application/json; charset=UTF-8')
        self.assertIn(expected_content_type, response.headerlist)

    def test_constructor_headerlist_with_add_header(self):
        response = JSONResponse({'foo': 'bar'}, headers={'key1': 'value1'})
        expected_content_type = ('key1', 'value1')
        self.assertIn(expected_content_type, response.headerlist)


class Jinja2TemplateTests(TestCase):
    @patch('kobin.app.current_config')
    def test_file(self, mock_config):
        """ Templates: Jinja2 file """
        config = load_config({'TEMPLATE_DIRS': TEMPLATE_DIRS})
        mock_config.return_value = config['TEMPLATE_ENVIRONMENT']
        response = TemplateResponse('jinja2.html', var='kobin')
        actual = response.body
        expected = [b"Hello kobin World."]
        self.assertEqual(actual, expected)


class RedirectResponseTests(TestCase):
    def test_constructor_body(self):
        response = RedirectResponse('/')
        self.assertEqual(response.body, [b''])

    def test_constructor_status_when_http10(self):
        test_env = {'HTTP_HOST': 'localhost', 'SERVER_PROTOCOL': 'HTTP/1.0'}
        app = Kobin()
        app(test_env, lambda x, y: None)
        response = RedirectResponse('/')
        self.assertEqual(response.status_code, 302)

    def test_constructor_status_when_http11(self):
        test_env = {'HTTP_HOST': 'localhost', 'SERVER_PROTOCOL': 'HTTP/1.1'}
        app = Kobin()
        app(test_env, lambda x, y: None)
        response = RedirectResponse('/')
        self.assertEqual(response.status_code, 303)

    def test_constructor_headerlist_has_location(self):
        test_env = {'HTTP_HOST': 'localhost', 'SERVER_PROTOCOL': 'HTTP/1.1'}
        app = Kobin()
        app(test_env, lambda x, y: None)
        response = RedirectResponse('/hello')
        expected_content_type = ('Location', 'http://localhost/hello')
        self.assertIn(expected_content_type, response.headerlist)
