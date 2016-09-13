import os
from unittest import TestCase
from unittest.mock import patch
from kobin.templates import render_template

TEMPLATE_DIRS = [os.path.join(os.path.dirname(__file__), 'templates')]


class Jinja2TemplateTests(TestCase):
    @patch('kobin.current_config')
    def test_file(self, mock_current_config):
        """ Templates: Jinja2 file """
        mock_current_config.return_value = {'TEMPLATE_DIRS': TEMPLATE_DIRS}
        actual = render_template('jinja2.html', var='kobin')
        expected = "Hello kobin World."
        self.assertEqual(actual, expected)
