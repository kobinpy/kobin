from unittest import TestCase
from unittest.mock import MagicMock

from kobin.environs import Request, Response


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

        self.assertEqual(request.POST['key1'], 'value1')

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

        self.assertEqual(request.POST['key1'], 'value1')
        self.assertEqual(request.POST['key2'], 'value2')

    def test_GET_a_parameter(self):
        request = Request({
            'REQUEST_METHOD': 'GET',
            'QUERY_STRING': 'key1=value1',
            'CONTENT_TYPE': 'text/plain',
            'CONTENT_LENGTH': '',
        })
        self.assertEqual(request.GET['key1'], 'value1')

    def test_GET_parameters(self):
        request = Request({
            'REQUEST_METHOD': 'GET',
            'QUERY_STRING': 'key1=value1&key2=value2',
            'CONTENT_TYPE': 'text/plain',
            'CONTENT_LENGTH': '',
        })
        self.assertEqual(request.GET['key1'], 'value1')
        self.assertEqual(request.GET['key2'], 'value2')

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


class ResponseTests(TestCase):
    def test_constructor_body(self):
        response = Response('')
        self.assertEqual('', response.body)

    def test_constructor_status(self):
        response = Response('Body', 200)
        self.assertEqual(response.status_code, 200)

    def test_set_status(self):
        response = Response()
        response.status = 200
        self.assertEqual(response.status, '200 OK')

    def test_constructor_headerlist(self):
        response = Response()
        expected_content_type = ('Content-Type', 'text/html; charset=UTF-8')
        self.assertIn(expected_content_type, response.headerlist)

    def test_constructor_headerlist_has_already_content_type(self):
        response = Response()
        response.add_header('Content-Type', 'application/json')
        expected_content_type = ('Content-Type', 'application/json')
        self.assertIn(expected_content_type, response.headerlist)
        expected_content_type = ('Content-Type', 'text/html; charset=UTF-8')
        self.assertNotIn(expected_content_type, response.headerlist)

    def test_add_header(self):
        response = Response()
        response.add_header('key', 'value')
        self.assertIn(('key', 'value'), response.headerlist)

    def test_constructor_headerlist_with_add_header(self):
        response = Response(headers={'key1': 'value1'})
        expected_content_type = ('key1', 'value1')
        self.assertIn(expected_content_type, response.headerlist)
