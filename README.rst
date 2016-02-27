=================================================
Kobin: a small and statically-typed web framework
=================================================

.. image:: https://travis-ci.org/c-bata/kobin.svg?branch=master
   :target: https://travis-ci.org/c-bata/kobin

.. image:: https://badge.fury.io/py/kobin.svg
   :target: https://badge.fury.io/py/kobin

.. image:: https://coveralls.io/repos/github/c-bata/kobin/badge.svg?branch=coveralls
   :target: https://coveralls.io/github/c-bata/kobin?branch=master

.. image:: https://codeclimate.com/github/c-bata/kobin/badges/gpa.svg
   :target: https://codeclimate.com/github/c-bata/kobin
   :alt: Code Climate

.. image:: https://readthedocs.org/projects/kobin/badge/?version=latest
   :target: http://kobin.readthedocs.org/en/latest/?badge=latest
   :alt: Documentation Status

**This library is a pre-release. Expect missing docs and breaking API changes.**

Some reasons you might want to use Kobin.

- **Statically-typed** web framework with PEP 0484(Type Hints).
- **Minimal source code** for solving your problems when you are troubled.
- Requires routing, jinja2 support, WSGI request and response wrapper and so on.


Requirements
------------

* Supported python version is 3.5 only.

Kobin Requires the following:

- Python 3.5

The following packages are optional:

- Jinja2
- gunicorn


Getting Started
===============

Installation
------------

::

    $ pip install kobin
    $ pip install gunicorn
    $ pip install jinja2


Usage
-----

.. code-block:: python

    from kobin import Kobin, request, response, template

    app = Kobin()
    app.config.update({
        'SERVER': 'gunicorn',
        'HOST': '127.0.0.1',
        'PORT': 8080,
    })

    @app.route('^/$')
    def index():
        return "Hello Kobin!"

    @app.route('^/tasks/(?P<task_id>\d+)/$')
    def task_detail(task_id: int):
        response.add_header('key', 'value')
        tasks = ('task1 is ...', 'task2 is ...', 'task3 is ...', )
        return template('task', request=request, task_id=task_id)

    if __name__ == '__main__':
        app.run()


License
=======

This software is licensed under the MIT License.

Resources
=========

* `Github <https://github.com/c-bata/kobin>`_
* `PyPI <https://pypi.python.org/pypi/kobin>`_
