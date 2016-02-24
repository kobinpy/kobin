=====
Kobin
=====

.. image:: https://travis-ci.org/c-bata/kobin.svg?branch=master
    :target: https://travis-ci.org/c-bata/kobin

**This library is a pre-release. Expect missing docs and breaking API changes.**

A lightweight web application framework for python3.5.

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

    from kobin import Kobin, template

    app = Kobin()

    @app.route('^/$')
    def index():
        return "Hello Kobin!"

    @app.route('^/users/(?P<name>\w+)/$')
    def hello(name: str):
        return template("hello", name=name)

    @app.route('^/tasks/(?P<task_id>\d+)/$')
    def task_detail(task_id: int):
        tasks = ('task1 is ...', 'task2 is ...', 'task3 is ...', )
        return template('task', task_id=task_id)

    if __name__ == '__main__':
        app.run()


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
