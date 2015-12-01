import os
from setuptools import setup, find_packages
from kobin import (
    __version__,
    __author__,
    __author_email__,
    __license__,
)

BASE_PATH = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(BASE_PATH, 'README.rst')).read()
CHANGES = open(os.path.join(BASE_PATH, 'CHANGES.rst')).read()

__classifiers__ = (
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries',
    'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
    'Topic :: Internet :: WWW/HTTP :: WSGI',
    'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    'Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware',
    'Topic :: Internet :: WWW/HTTP :: WSGI :: Server',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
)

setup(
    name='kobin',
    version=__version__,
    author=__author__,
    author_email=__author_email__,
    url='https://github.com/c-bata/kobin',
    description='A very simple web application framework.',
    long_description=README + '\n\n' + CHANGES,
    classifiers=__classifiers__,
    packages=find_packages(exclude=['test*']),
    install_requirements=[],
    keywords='web framework waf',
    license=__license__,
    include_package_data=True,
    test_suite='tests',
)
