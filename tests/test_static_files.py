from unittest import TestCase

from . import STATIC_DIRS
from kobin.static_files import static_file
from kobin import Kobin, response
from kobin.exceptions import HTTPError


class StaticFilesTests(TestCase):
    def setUp(self):
        self.app = Kobin()

    def test_return_static_file(self):
        actual = static_file('static.css', STATIC_DIRS[0])
        expected = 'body { color: black; }\n'.encode('utf-8')
        self.assertEqual(actual, expected)

    def test_static_file_404_not_found(self):
        self.assertRaises(HTTPError, static_file, 'not_found.png', STATIC_DIRS[0])

    def test_exist_last_modified_in_headers(self):
        static_file('static.css', STATIC_DIRS[0])
        self.assertIn('Last-Modified', response._headers)

    def test_content_length(self):
        expected_content_length = str(23)
        static_file('static.css', STATIC_DIRS[0])
        actual_content_length = response._headers['Content-Length']
        self.assertIn(expected_content_length, actual_content_length)

    def test_content_type(self):
        expected_content_type = 'text/css; charset=UTF-8'
        static_file('static.css', STATIC_DIRS[0])
        actual_content_type = response._headers['Content-Type']
        self.assertIn(expected_content_type, actual_content_type)
