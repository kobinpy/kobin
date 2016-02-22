import os
from unittest import TestCase
from kobin.templates import Jinja2Template


class Jinja2TemplateTests(TestCase):
    def test_file(self):
        """ Templates: Jinja2 file """
        j2 = Jinja2Template(name='jinja2', template_dirs=['./templates'],
                            root=os.path.dirname(os.path.abspath(__file__)))
        actual = j2.render(var='kobin')
        expected = "Hello kobin World."
        self.assertEqual(actual, expected)
