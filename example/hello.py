from kobin import Kobin, request, response, template

app = Kobin()
app.config.load_from_pyfile('./config.py')


@app.route('^/$')
def index():
    response.add_header("hoge", "fuga")
    return template('hello_jinja2', name='Kobin')


@app.route('^/years/(?P<year>\d{4})$')
def casted_year(year: int):
    return 'A "year" argument is integer? {}'.format(isinstance(year, int))


@app.route('^/user/(?P<name>\w+)$')
def hello(name: str):
    return """
    <p>Hello {}</p>
    <p>Request Path: {}</p>
    <p>Response Headers: {}</p>
    """.format(name, request.path, str(response.headerlist))

if __name__ == '__main__':
    app.run()
