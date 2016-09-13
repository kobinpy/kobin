from jinja2 import Environment, FileSystemLoader  # type: ignore


def render_template(template_name: str, **kwargs) -> str:
    """ Get a rendered template as string iterator. """
    from . import current_config
    env = Environment(loader=FileSystemLoader(current_config()['TEMPLATE_DIRS']))
    return env.get_template(template_name).render(**kwargs)
