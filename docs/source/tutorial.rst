========
Tutorial
========

Installation
============

In this tutorial, we will use Python 3.6.

.. code-block:: console

   $ python --version
   Python 3.6.0b4
   $ pip install -U pip
   $ pip install kobin wsgicli

* Kobin: WSGI Framework
* WSGICLI: Command line tools for developing your WSGI Application


Your first kobin app
====================

Let's make Kobin's application.
Please create a ``main.py``:

.. code-block:: python

   from kobin import Kobin, Response, JSONResponse
   app = Kobin()

   @app.route('/')
   def index() -> Response:
       return Response("Hello World!")

   @app.route('/users/{user_id}')
   def say_hello(user_id: int) -> JSONResponse:
       return JSONResponse({
           "message": f"Hello user{user_id}!"
       })

For those who have used the WSGI framework such as Bottle and Flask,
it may be familiar with this code.
One distinctive feature is the existence of type hints.
Kobin casts the URL variable based on the type hinting and passes it to the View function.

Let's actually move it.
There are several ways to run WSGI's application.
In the development environment we recommend a command line tool called ``wsgicli``.

.. code-block:: console

   $ wsgicli run main.py app
   Start: 127.0.0.1:8000

When the server starts up successfully, let's access following urls.

- http://localhost:8000/
- http://localhost:8000/users/1

Did you see any message? Congratulations!


Deploy to production
====================

In a production, let's use ``gunicorn`` instead of using ``wsgicli`` for a performance reasons.

.. code-block:: console

   $ pip install gunicorn
   $ gunicorn main:app

Then please try accessing your website.
If you use the function of static file serving in wsgicli, maybe the layout and styles have gone wrong.
Actually, gunicorn doesn't have the function of serving static content such as CSS, JS, and image files.
Generally, the reverse proxy server such as Nginx is used for serving static content in production
(See `Serving Static Content - Nginx <https://www.nginx.com/resources/admin-guide/serving-static-content/>`_ .

If you absolutely need to serve static contents in Python's application side (ex: Using Heroku),
Please use `kobinpy/wsgi-static-middleware <https://github.com/kobinpy/wsgi-static-middleware>`_ .


Next Step
=========

More practical example is `kobin-example <https://github.com/kobinpy/kobin-example>`_ .
If you want to know the best practices in Kobin, Please check it.

.. image:: _static/kobin-example.gif
   :alt: Kobin Example Demo Animation
   :align: center
