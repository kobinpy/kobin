from typing import List, Dict, Any, Callable
import os
import functools

from .exceptions import HTTPError


def load_file(name: str, directories: List[str]) -> str:
    for directory in directories:
        if not os.path.isabs(directory):
            directory = os.path.abspath(directory) + os.sep
        file = os.path.join(directory, name)
        if os.path.exists(file) and os.path.isfile(file) and os.access(file, os.R_OK):
            return file
        # TODO: if not os.access: raise HTTPError(403, "You do not have permission to access this file.")
    raise HTTPError(404, "{name} not found.".format(name=name))


class TemplateMixin:
    extension = 'html'  # type: str
    settings = {}  # type: Dict[str, Any]  # used in parepare()
    defaults = {}  # type: Dict[str, Any]  # used in render()

    def __init__(self, name: str, encoding: str='utf8', **settings) -> None:
        """ Create a new template. """
        from . import current_config  # type: ignore
        self.name = name
        config = current_config()  # type: ignore
        self.template_dirs = config['TEMPLATE_DIRS']  # type: List[str]
        self.filename = self.search(self.name, self.template_dirs)  # type: str

        self.encoding = encoding
        self.settings = self.settings.copy()
        self.prepare(**self.settings)

    @classmethod
    def search(cls, name: str, template_dirs: List[str]) -> str:
        """ Search name in all directories specified in lookup. """
        filename = '{name}.{ext}'.format(name=name, ext=cls.extension)
        return load_file(filename, template_dirs)

    def prepare(self, **options):
        raise NotImplementedError

    def render(self, *args, **kwargs):
        raise NotImplementedError


class Jinja2Template(TemplateMixin):
    def prepare(self, filters: Dict=None, tests: Dict=None, globals: Dict={}, **kwargs) -> None:
        from jinja2 import Environment, FunctionLoader  # type: ignore
        self.env = Environment(loader=FunctionLoader(self.loader), **kwargs)
        if filters:
            self.env.filters.update(filters)
        if tests:
            self.env.tests.update(tests)
        if globals:
            self.env.globals.update(globals)
        self.tpl = self.env.get_template(self.filename)

    def render(self, *args, **kwargs) -> str:
        for dictarg in args:
            kwargs.update(dictarg)
        _defaults = self.defaults.copy()
        _defaults.update(kwargs)
        return self.tpl.render(**_defaults)

    def loader(self, name: str) -> str:
        if name == self.filename:
            fname = name
        else:
            fname = self.search(name, self.template_dirs)
        if not fname:
            return  # type: ignore
        with open(fname, "rb") as f:
            return f.read().decode(self.encoding)


def template(template_name: str, **kwargs) -> str:
    """ Get a rendered template as string iterator. """
    adapter = kwargs.pop('template_adapter', Jinja2Template)
    return adapter(name=template_name).render(**kwargs)

jinja2_template = functools.partial(template, adapter=Jinja2Template)
