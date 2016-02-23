import os
from unittest import TestCase
from kobin.templates import Jinja2Template

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class LoadFileTests(TestCase):
    def test_load_file(self):
        pass

    def test_raise_403_do_not_have_access_permission(self):
        pass

    def test_raise_404_because_file_does_not_exist(self):
        pass

    def test_raise_404_because_it_is_not_file(self):
        pass


class Jinja2TemplateTests(TestCase):
    def test_file(self):
        """ Templates: Jinja2 file """
        j2 = Jinja2Template(name='jinja2', template_dirs=[os.path.join(BASE_DIR, './templates')])
        actual = j2.render(var='kobin')
        expected = "Hello kobin World."
        self.assertEqual(actual, expected)
