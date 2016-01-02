=====
Kobin
=====

A very simple web application framework for python3.5.
This library has no dependencies other than the Python Standard Libraries.

* Routing
* Template
* Development Server

Getting Started
===============

Installation
------------

::

    $ pip install kobin

Usage
-----

.. code-block:: python

    from kobin import Kobin

    app = Kobin()

    @app.route('^/$')
    def index():
        return "Hello Kobin!"


    @app.route('^/user/(?P<name>\w+)/$')
    def hello(name):
        return "Hello {}".format(name)

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
