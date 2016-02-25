import os
from typing import List

BASE_DIR = os.path.abspath('.')
TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]  # type: List[str]
STATIC_DIRS = [os.path.join(BASE_DIR, 'static')]  # type: List[str]

from .app import Kobin
from .environs import request, response
from .templates import template, jinja2_template
