from jinja2 import Environment, FileSystemLoader  # type: ignore


def render_template(template_name: str, **kwargs) -> str:
    """ Get a rendered template as string iterator. """
    from . import current_config  # type: ignore
    env = Environment(loader=FileSystemLoader(current_config()['TEMPLATE_DIRS']))  # type: ignore
    return env.get_template(template_name).render(**kwargs)
