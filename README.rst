=====
Kobin
=====

A very simple web application framework for python3.5.
This library has no dependencies other than the Python Standard Library.

* Routing
* Template
* Server

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

    @app.route('/')
    def hello():
        return "Hello World"

    @app.route('/hoge')
    def hello():
        return "Hello HOGEHOGE"

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
