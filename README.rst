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


`Kobin <https://kobin.readthedocs.org/>`_ is a small and statically-typed WSGI micro web framework for Python.
**This library is a pre-release. Expect missing docs and breaking API changes.**
Kobin has following features.

- **Statically-typed** web framework with PEP 0484(Type Hints).
- **Lightweight** implementations for solving your problems easily.
- Kobin provides Routing, WSGI request and response wrapper, Jinja2 template adapter and several useful utilities.
- Convert URL variables types using Type Hints.


Getting started
===============

Installation
------------

.. code-block:: console

   $ pip install kobin

Hello World with Kobin
----------------------

.. code-block:: python

   from kobin import Kobin
   app = Kobin()

   @app.route('/')
   def hello() -> str:
       return "Hello World"

   @app.route('/users/{user_id}')
   def hello(user_id: int) -> str:
       return "Hello {}!!".format(user_id)


Run server
----------

**Development**

.. code-block:: console

   $ wsgicli main.py app --reload

**Production**

.. code-block:: console

   $ pip install gunicorn
   $ gunicorn main:app

Requirements
============

Kobin requires the following:

- Python 3.5
- Jinja2
- wsgicli


Resources
=========

* `Documentation (English) <https://kobin.readthedocs.org/en/latest/>`_
* `Documentation (日本語) <https://kobin.readthedocs.org/ja/latest/>`_
* `Github <https://github.com/kobinpy/kobin>`_
* `PyPI <https://pypi.python.org/pypi/kobin>`_


License
=======

This software is licensed under the MIT License.
