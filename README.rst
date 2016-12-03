=====
Kobin
=====

.. image:: https://travis-ci.org/kobinpy/kobin.svg?branch=master
   :target: https://travis-ci.org/kobinpy/kobin

.. image:: https://badge.fury.io/py/kobin.svg
   :target: https://badge.fury.io/py/kobin

.. image:: https://coveralls.io/repos/github/kobinpy/kobin/badge.svg?branch=coveralls
   :target: https://coveralls.io/github/kobinpy/kobin?branch=master

.. image:: https://codeclimate.com/github/c-bata/kobin/badges/gpa.svg
   :target: https://codeclimate.com/github/kobinpy/kobin
   :alt: Code Climate

.. image:: https://readthedocs.org/projects/kobin/badge/?version=latest
   :target: http://kobin.readthedocs.org/en/latest/?badge=latest
   :alt: Documentation Status


A Minimal WSGI Framework to develop your web application comfortably.
**This library is a pre-release. Expect missing docs and breaking API changes.**

Kobin has following features.

- Decorator based Routing System exploited Type Hints.
- WSGI request and response Wrapper.
- Provide type annotations from stub files.
- and other convenient utilities...

And Kobin has **NO** following features:

- *WSGI Server Adapters*: Please use WSGICLI or Gunicorn CLI.
- *Serving static contents*: Please use WSGICLI and Nginx.
- *Template Engine*: But Kobin provides template adapter.

Getting started
===============

Installation
------------

.. code-block:: console

   $ pip install kobin

Hello World with Kobin
----------------------

.. code-block:: python

   from kobin import Kobin, Response, JSONResponse
   app = Kobin()

   @app.route('/')
   def hello() -> Response:
       return Response("Hello World")

   @app.route('/users/{user_id}')
   def hello(user_id: int) -> JSONResponse:
       return JSONResponse({
           "message": "Hello {}!!".format(user_id)
       })


Run server
----------

**Development**

.. code-block:: console

   $ pip install wsgicli
   $ wsgicli main.py app --reload

**Production**

.. code-block:: console

   $ pip install gunicorn
   $ gunicorn main:app


Requirements
============

Kobin requires the following:

- Python 3.5 or 3.6(beta)
- Jinja2


Resources
=========

* `Documentation (English) <https://kobin.readthedocs.org/en/latest/>`_
* `Documentation (日本語) <https://kobin.readthedocs.org/ja/latest/>`_
* `Github <https://github.com/kobinpy/kobin>`_
* `PyPI <https://pypi.python.org/pypi/kobin>`_


License
=======

This software is licensed under the MIT License.
