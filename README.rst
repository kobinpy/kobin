=====
Kobin
=====

.. image:: https://travis-ci.org/c-bata/kobin.svg?branch=master
    :target: https://travis-ci.org/c-bata/kobin

.. image:: https://badge.fury.io/py/kobin.svg
    :target: https://badge.fury.io/py/kobin

**This library is a pre-release. Expect missing docs and breaking API changes.**

Kobin is small and statically-typed web framework for python3.5.

* Routing
* Request and Response object
* Template loader for Jinja2
* Static files server

Getting Started
===============

Installation
------------

::

    $ pip install kobin

Usage
-----

.. code-block:: python

    from kobin import Kobin, request, response, template

    app = Kobin()

    @app.route('^/$')
    def index():
        return "Hello Kobin!"

    @app.route('^/tasks/(?P<task_id>\d+)/$')
    def task_detail(task_id: int):
        response.add_header('key', 'value')
        tasks = ('task1 is ...', 'task2 is ...', 'task3 is ...', )
        return template('task', request=request, task_id=task_id)

    if __name__ == '__main__':
        app.run(host='127.0.0.1', port=8080)


Requirements
============

* Supported python version is 3.5 only.

License
=======

This software is licensed under the MIT License.

Resources
=========

* `Github <http://https://github.com/c-bata/kobin>`_
* `PyPI <https://pypi.python.org/pypi/kobin>`_
