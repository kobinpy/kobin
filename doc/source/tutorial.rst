========
Tutorial
========

Installation
============

Install using pip, including any optional packages you want..

::

    $ pip install kobin
    $ pip install jinja2
    $ pip install gunicorn

We're ready to create our web site now.


Creating web site
=================

`app.py`

.. code-block:: python

    from kobin import Kobin, request, response, template

    app = Kobin()
    app.config.load_from_pyfile('config.py')

    @app.route('^/$')
    def index():
        response.add_header('key', 'value')
        return template('index')

    if __name__ == '__main__':
        app.run()


`config.py`

.. code-block:: python

    import os

    BASE_DIR = os.path.dirname(os.path.abspath(__name__))
    TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
    STATIC_URL = '/static/'

    PORT = 8080
    HOST = '127.0.0.1'
    SERVER = 'gunicorn'


`static/index.html`

.. code-block:: html

    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Hello Kobin</title>
        <link rel="shortcut icon" href="/static/favicon.ico">
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
        <header>
            <div class="container">
                <h1 style="color: #eeeeee">Kobin: lightweight web application framework.</h1>
            </div>
        </header>
        <main>
            <div class="container">
                <p>Hello {{ name }}! with Jinja2 template.</p>
            </div>
        </main>
        <footer>
            <p style="text-align: center;">Powered by Kobin.</p>
        </footer>
    </body>
    </html>

`static/style.css`

.. code-block:: css

    body {
        display: flex;
        min-height: 100vh;
        flex-direction: column;
        margin:0;
    }
    header {
        background-color: #333333;
    }
    main {
        flex: 1;
    }
    footer {
        margin: 30px 0;
    }
    .container {
        max-width: 980px;
        width: 100%;
        margin: 0 auto;
    }
