import os
from unittest import TestCase
from unittest.mock import patch

from kobin.exceptions import HTTPError
from kobin.templates import Jinja2Template, load_file

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class LoadFileTests(TestCase):
    def setUp(self):
        self.template_dirs = [os.path.join(BASE_DIR, 'templates')]

    def test_load_file(self):
        actual = load_file('jinja2.html', self.template_dirs)
        expected = os.path.join(self.template_dirs[0], 'jinja2.html')
        self.assertEqual(actual, expected)

    @patch('os.access')
    def test_raise_403_do_not_have_access_permission(self, mock_os_access):
        mock_os_access.return_value = False
        input_args = {
            'name': 'jinja2.html',
            'directories': self.template_dirs,
        }
        self.assertRaises(HTTPError, load_file, **input_args)

    def test_raise_404_because_file_does_not_exist(self):
        input_args = {
            'name': 'does_not_exist.html',
            'directories': [os.path.join(BASE_DIR, 'templates')]
        }
        self.assertRaises(HTTPError, load_file, **input_args)

    def test_raise_404_because_it_is_not_file(self):
        input_args = {
            'name': 'this_is_not_file.html',
            'directories': [os.path.join(BASE_DIR, 'templates')]
        }
        self.assertRaises(HTTPError, load_file, **input_args)


class Jinja2TemplateTests(TestCase):
    def test_file(self):
        """ Templates: Jinja2 file """
        j2 = Jinja2Template(name='jinja2', template_dirs=[os.path.join(BASE_DIR, './templates')])
        actual = j2.render(var='kobin')
        expected = "Hello kobin World."
        self.assertEqual(actual, expected)
