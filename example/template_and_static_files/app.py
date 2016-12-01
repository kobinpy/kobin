from kobin import Kobin, request, Response, TemplateResponse

app = Kobin()
app.config.load_from_pyfile('config.py')


@app.route('/')
def index():
    return TemplateResponse(
        'hello_jinja2.html', name='Kobin', headers={'foo': 'bar'}
    )


@app.route('/user/{name}')
def hello(name: str):
    body = """
    <p>Hello {}</p>
    <p>Request Path: {}</p>
    """.format(name, request.path)
    return Response(body)
