from unittest import TestCase
from kobin.environs import Request


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
