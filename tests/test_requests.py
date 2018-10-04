from datetime import timedelta, datetime
import freezegun
import os
from unittest import TestCase
from unittest.mock import MagicMock, patch

from kobin.requests import (
    Request, _split_into_mimetype_and_priority, _parse_and_sort_accept_header, accept_best_match
)
from kobin.responses import BaseResponse

TEMPLATE_DIRS = [os.path.join(os.path.dirname(__file__), 'templates')]


class RequestTests(TestCase):
    def test_initialized(self):
        env = {'hoge': 'HOGE'}
        request = Request(env)
        self.assertEqual(request['hoge'], 'HOGE')

    def test_get(self):
        request = Request({'hoge': 'HOGE'})
        self.assertEqual(request.get('hoge'), 'HOGE')

    def test_getitem(self):
        request = Request({'hoge': 'HOGE'})
        self.assertEqual(request['hoge'], 'HOGE')

    def test_get_default_value(self):
        request = Request({})
        self.assertEqual(request.get('hoge', 'HOGE'), 'HOGE')

    def test_path_property(self):
        request = Request({'PATH_INFO': '/hoge'})
        self.assertEqual(request.path, '/hoge')

    def test_path_property_stripped_last_slash(self):
        request = Request({'PATH_INFO': 'hoge'})
        self.assertEqual(request.path, '/hoge')

    def test_method_name_to_uppercase(self):
        self.assertEqual(Request({'REQUEST_METHOD': 'get'}).method, 'GET')
        self.assertEqual(Request({'REQUEST_METHOD': 'Post'}).method, 'POST')

    def test_POST_a_parameter(self):
        wsgi_input_mock = MagicMock()
        wsgi_input_mock.read.return_value = b'key1=value1'

        request = Request({
            'REQUEST_METHOD': 'POST',
            'QUERY_STRING': '',
            'wsgi.input': wsgi_input_mock,
            'CONTENT_TYPE': 'application/x-www-form-urlencoded',
            'CONTENT_LENGTH': len(b'key1=value1'),
        })

        self.assertEqual(request.forms['key1'], 'value1')

    def test_POST_parameters(self):
        wsgi_input_mock = MagicMock()
        wsgi_input_mock.read.return_value = b'key1=value1&key2=value2'

        request = Request({
            'REQUEST_METHOD': 'POST',
            'QUERY_STRING': '',
            'wsgi.input': wsgi_input_mock,
            'CONTENT_TYPE': 'application/x-www-form-urlencoded',
            'CONTENT_LENGTH': len(b'key1=value1&key2=value2'),
        })

        self.assertEqual(request.forms['key1'], 'value1')
        self.assertEqual(request.forms['key2'], 'value2')

    def test_GET_a_parameter(self):
        request = Request({
            'REQUEST_METHOD': 'GET',
            'QUERY_STRING': 'key1=value1',
            'CONTENT_TYPE': 'text/plain',
            'CONTENT_LENGTH': '',
        })
        self.assertEqual(request.query['key1'], 'value1')

    def test_GET_parameters(self):
        request = Request({
            'REQUEST_METHOD': 'GET',
            'QUERY_STRING': 'key1=value1&key2=value2',
            'CONTENT_TYPE': 'text/plain',
            'CONTENT_LENGTH': '',
        })
        self.assertEqual(request.query['key1'], 'value1')
        self.assertEqual(request.query['key2'], 'value2')

    def test_raw_body(self):
        wsgi_input_mock = MagicMock()
        wsgi_input_mock.read.return_value = b'{"key1": "value1"}'
        request = Request({
            'REQUEST_METHOD': 'POST',
            'QUERY_STRING': '',
            'wsgi.input': wsgi_input_mock,
            'CONTENT_TYPE': 'application/json',
            'CONTENT_LENGTH': len(b'{"key1": "value1"}'),
        })
        self.assertEqual(request.raw_body, b'{"key1": "value1"}')

    def test_raw_body_with_empty_string_content_length(self):
        wsgi_input_mock = MagicMock()
        wsgi_input_mock.read.return_value = b''
        request = Request({
            'REQUEST_METHOD': 'POST',
            'QUERY_STRING': '',
            'wsgi.input': wsgi_input_mock,
            'CONTENT_TYPE': 'text/plain',
            'CONTENT_LENGTH': '',
        })
        self.assertEqual(request.raw_body, b'')

    def test_body(self):
        wsgi_input_mock = MagicMock()
        wsgi_input_mock.read.return_value = b'{"key1": "value1"}'
        request = Request({
            'REQUEST_METHOD': 'POST',
            'QUERY_STRING': '',
            'wsgi.input': wsgi_input_mock,
            'CONTENT_TYPE': 'application/json',
            'CONTENT_LENGTH': len(b'{"key1": "value1"}'),
        })
        self.assertEqual(request.body, '{"key1": "value1"}')

    def test_json(self):
        wsgi_input_mock = MagicMock()
        wsgi_input_mock.read.return_value = b'{"key1": "value1"}'
        request = Request({
            'REQUEST_METHOD': 'POST',
            'QUERY_STRING': '',
            'wsgi.input': wsgi_input_mock,
            'CONTENT_TYPE': 'application/json',
            'CONTENT_LENGTH': len(b'{"key1": "value1"}'),
        })
        self.assertEqual(request.json["key1"], "value1")

    def test_url(self):
        request = Request({
            'HTTP_X_FORWARDED_PROTO': 'http',
            'QUERY_STRING': 'key1=value1&key2=value2',
            'HTTP_X_FORWARDED_HOST': 'localhost',
            'PATH_INFO': '/hoge',
        })
        actual = request.url
        self.assertEqual(actual, "http://localhost/hoge?key1=value1&key2=value2")

    def test_headers(self):
        request = Request({'HTTP_FOO': 'Bar', 'QUERY_STRING': 'key1=value1'})
        self.assertEqual(request.headers['FOO'], 'Bar')


class AcceptBestMatchTests(TestCase):
    def test_split_into_mimetype_and_priority_without_priority(self):
        item = 'text/*'
        actual = _split_into_mimetype_and_priority(item)
        expected = ('text/*', 1.0)
        self.assertEqual(actual, expected)

    def test_split_into_mimetype_and_priority_with_priority(self):
        item = 'application/json;q=0.5'
        actual = _split_into_mimetype_and_priority(item)
        expected = ('application/json', 0.5)
        self.assertEqual(actual, expected)

    def test_parse_and_sort_accept_header(self):
        accept_header = 'application/json;q=0.5, text/html'
        actual = _parse_and_sort_accept_header(accept_header)
        expected = [
            ('text/html', 1.0),
            ('application/json', 0.5)
        ]
        self.assertEqual(actual, expected)

    def test_best_match_without_priority(self):
        accept_header = 'application/json, application/xml'
        expected = 'application/json'
        actual = accept_best_match(accept_header, ['application/json'])
        self.assertEqual(actual, expected)

    def test_best_match_with_priority(self):
        accept_header = 'text/*;q=0.9, */;q=0.1, audio/mpeg, application/xml;q=0.'
        expected = 'application/json'
        actual = accept_best_match(accept_header, ['application/json'])
        self.assertEqual(actual, expected)

    def test_best_match_with_priority_and_wildcard(self):
        accept_header = 'application/json;q=0.5, text/*, */*;q=0.1'
        actual = accept_best_match(accept_header, ['application/json', 'text/plain'])
        expected = 'text/plain'
        self.assertEqual(actual, expected)


class CookieTests(TestCase):
    # Set Cookie Tests in BaseResponse Class
    def test_set_cookie(self):
        response = BaseResponse()
        response.set_cookie('foo', 'bar')
        expected_set_cookie = ('Set-Cookie', 'foo=bar; Path=/')
        self.assertIn(expected_set_cookie, response.headerlist)

    def test_set_cookie_with_max_age(self):
        response = BaseResponse()
        response.set_cookie('foo', 'bar', max_age=timedelta(seconds=10), path=None)
        expected_set_cookie = ('Set-Cookie', 'foo=bar; Max-Age=10')
        self.assertIn(expected_set_cookie, response.headerlist)

    def test_set_cookie_with_expires(self):
        response = BaseResponse()
        response.set_cookie('foo', 'bar', expires=datetime(2017, 1, 1, 0, 0, 0), path=None)
        expected_set_cookie = ('Set-Cookie', 'foo=bar; expires=Sun, 01 Jan 2017 00:00:00 GMT')
        self.assertIn(expected_set_cookie, response.headerlist)

    def test_set_cookie_with_path(self):
        response = BaseResponse()
        response.set_cookie('foo', 'bar', path='/foo')
        expected_set_cookie = ('Set-Cookie', 'foo=bar; Path=/foo')
        self.assertIn(expected_set_cookie, response.headerlist)

    # Get Cookie Tests in Request Class
    def test_cookies_property_has_nothing(self):
        request = Request({})
        self.assertEqual(len(request.cookies), 0)

    def test_cookies_property_has_an_item(self):
        request = Request({'HTTP_COOKIE': 'foo="bar"'})
        self.assertEqual(len(request.cookies), 1)

    def test_get_cookie(self):
        request = Request({'HTTP_COOKIE': 'foo="bar"'})
        actual = request.get_cookie("foo")
        expected = 'bar'
        self.assertEqual(actual, expected)

    # Delete Cookie Tests in Request Class
    @freezegun.freeze_time('2017-01-01 00:00:00')
    def test_delete_cookie(self):
        response = BaseResponse()
        response.delete_cookie('foo')
        expected_set_cookie = (
            'Set-Cookie',
            'foo=""; expires=Sun, 01 Jan 2017 00:00:00 GMT; Max-Age=-1; Path=/')
        self.assertIn(expected_set_cookie, response.headerlist)

    # Get and Set Cookie Tests with secret
    def test_set_cookie_with_secret(self):
        response = BaseResponse()
        response.set_cookie('foo', 'bar', secret='secretkey', path=None)
        expected_set_cookie = ('Set-Cookie', 'foo="!VzhGFLGcW+5OMs1s4beLXaqFxAUwgHdWkH5fgapghoI='
                                             '?gASVDwAAAAAAAACMA2Zvb5SMA2JhcpSGlC4="')
        self.assertIn(expected_set_cookie, response.headerlist)

    def test_get_cookie_with_secret(self):
        request = Request({'HTTP_COOKIE': 'foo="!VzhGFLGcW+5OMs1s4beLXaqFxAUwgHdWkH5fgapghoI='
                                          '?gASVDwAAAAAAAACMA2Zvb5SMA2JhcpSGlC4="'})
        actual = request.get_cookie("foo", secret='secretkey')
        expected = 'bar'
        self.assertEqual(actual, expected)

    @patch('kobin.app.current_config')
    def test_set_cookie_with_secret_in_config(self, mock_current_config):
        mock_current_config.return_value = "secretkey"
        response = BaseResponse()
        response.set_cookie('foo', 'bar', path=None)
        expected_set_cookie = ('Set-Cookie', 'foo="!VzhGFLGcW+5OMs1s4beLXaqFxAUwgHdWkH5fgapghoI='
                                             '?gASVDwAAAAAAAACMA2Zvb5SMA2JhcpSGlC4="')
        self.assertIn(expected_set_cookie, response.headerlist)
