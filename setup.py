import os
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

BASE_PATH = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(BASE_PATH, 'README.rst')).read()

__version__ = '0.1.6'
__author__ = 'Masashi Shibata <contact@c-bata.link>'
__author_email__ = 'contact@c-bata.link'
__license__ = 'MIT License'
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
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3 :: Only',
)


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    name='kobin',
    version=__version__,
    author=__author__,
    author_email=__author_email__,
    url='https://github.com/kobinpy/kobin',
    description='A Minimal WSGI Framework to develop your web application comfortably',
    long_description=README,
    classifiers=__classifiers__,
    packages=find_packages(exclude=['test*']),
    install_requires=[],
    keywords='web framework wsgi',
    license=__license__,
    include_package_data=True,
    test_suite='tests',
    tests_require=['pytest'],
    cmdclass={'test': PyTest},
)
