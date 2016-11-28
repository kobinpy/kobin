import os
from unittest import TestCase
from unittest.mock import patch

from jinja2 import Environment, FileSystemLoader
from kobin import Kobin
from kobin.templates import render_template

TEMPLATE_DIRS = [os.path.join(os.path.dirname(__file__), 'templates')]


class Jinja2TemplateTests(TestCase):
    def setUp(self):
        self.app = Kobin()
        self.app.config['TEMPLATE_DIRS'] = TEMPLATE_DIRS

    @patch('kobin.current_config')
    def test_file(self, mock_current_config):
        """ Templates: Jinja2 file """
        mock_current_config.return_value = {
            'JINJA2_ENV': Environment(loader=FileSystemLoader(TEMPLATE_DIRS))
        }
        actual = render_template('jinja2.html', var='kobin')
        expected = "Hello kobin World."
        self.assertEqual(actual, expected)
