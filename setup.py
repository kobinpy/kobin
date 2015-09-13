import os
from setuptools import setup

__author__ = 'Masashi Shibata <contact@c-bata.link>'
__version__ = '0.0.0'

BASE_PATH = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(BASE_PATH, 'README.rst')).read()
CHANGES = open(os.path.join(BASE_PATH, 'CHANGES.rst')).read()

setup(
    name='kobin',
    version=__version__,
    author=__author__,
    author_email='contact@c-bata.link',
    url='https://github.com/c-bata/kobin',
    description='A very simple web application framework.',
    long_description=README + '\n\n' + CHANGES,
    package=['kobin'],
    install_requirements=[],
    keywords=['web', 'framework', 'waf'],
    license='MIT License',
    include_package_data=True,
    test_suite='tests',
)
