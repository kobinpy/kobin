def render_template(template_name: str, **kwargs) -> str:
    """ Get a rendered template as string iterator. """
    from . import current_config  # type: ignore
    env = current_config()['JINJA2_ENV']  # type: ignore
    return env.get_template(template_name).render(**kwargs)
