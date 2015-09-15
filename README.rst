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

    from kobin import route, run, template

    @route('/hello/<name>')
    def index(name):
        return template('<b>Hello {{name}}</b>!', name=name)

    run(host='localhost', port=8080)


Requirements
============

* Supported python version is 3.5 only.

License
=======

This software is licensed under the MIT License.

Resources
=========

* `Github <http://https://github.com/c-bata/kobin>`_
