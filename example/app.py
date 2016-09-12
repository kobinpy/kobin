from kobin import Kobin, request, response, template
from wsgi_static_middleware import StaticMiddleware

app = Kobin()
app.config.load_from_pyfile('config.py')


@app.route('/')
def index():
    response.headers.add_header("hoge", "fuga")
    return template('hello_jinja2', name='Kobin')


@app.route('/user/{name}')
def hello(name: str):
    return """
    <p>Hello {}</p>
    <p>Request Path: {}</p>
    <p>Response Headers: {}</p>
    """.format(name, request.path, str(response.headerlist))

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    app = StaticMiddleware(app, static_root=app.config['STATIC_URL'],
                           static_dirs=app.config['STATICFILES_DIRS'])
    httpd = make_server('', 8080, app)
    httpd.serve_forever()
