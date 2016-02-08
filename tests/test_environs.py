from unittest import TestCase
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
        self.assertEqual(response.status_line, '200 OK')

    def test_constructor_headerlist(self):
        response = Response()
        expected_content_type = ('Content-Type', 'text/html; charset=UTF-8')
        self.assertIn(expected_content_type, response.headerlist)

    def test_add_header(self):
        response = Response()
        response.add_header('key', 'value')
        self.assertIn(('key', 'value'), response.headerlist)

    def test_constructor_headerlist_with_add_header(self):
        response = Response(headers={'key1': 'value1'})
        expected_content_type = ('key1', 'value1')
        self.assertIn(expected_content_type, response.headerlist)
