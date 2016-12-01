from kobin import Kobin, request, response, render_template

app = Kobin()
app.config.load_from_pyfile('config.py')


@app.route('/')
def index():
    response.headers.add_header("hoge", "fuga")
    return render_template('hello_jinja2.html', name='Kobin')


@app.route('/user/{name}')
def hello(name: str):
    return """
    <p>Hello {}</p>
    <p>Request Path: {}</p>
    <p>Response Headers: {}</p>
    """.format(name, request.path, str(response.headerlist))
