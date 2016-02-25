import os
from unittest import TestCase
from unittest.mock import patch
from kobin.exceptions import HTTPError
from kobin.templates import Jinja2Template, load_file

TEMPLATE_DIRS = [os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')]


class LoadFileTests(TestCase):
    def test_load_file(self):
        actual = load_file('jinja2.html', TEMPLATE_DIRS)
        expected = os.path.join(TEMPLATE_DIRS[0], 'jinja2.html')
        self.assertEqual(actual, expected)

    @patch('os.access')
    def test_raise_403_do_not_have_access_permission(self, mock_os_access):
        mock_os_access.return_value = False
        self.assertRaises(HTTPError, load_file,
                          name='jinja2.html', directories=TEMPLATE_DIRS)

    def test_raise_404_because_file_does_not_exist(self):
        self.assertRaises(HTTPError, load_file,
                          name='does_not_exist.html', directories=TEMPLATE_DIRS)

    def test_raise_404_because_it_is_not_file(self):
        self.assertRaises(HTTPError, load_file,
                          name='this_is_not_file.html', directories=TEMPLATE_DIRS)


class Jinja2TemplateTests(TestCase):
    @patch('kobin.current_config')
    def test_file(self, mock_current_config):
        """ Templates: Jinja2 file """
        mock_current_config.return_value = {'TEMPLATE_DIRS': TEMPLATE_DIRS}
        j2 = Jinja2Template(name='jinja2', template_dirs=TEMPLATE_DIRS)
        actual = j2.render(var='kobin')
        expected = "Hello kobin World."
        self.assertEqual(actual, expected)
