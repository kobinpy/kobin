from kobin import Kobin, request, Response, TemplateResponse, load_config_from_pyfile

config = load_config_from_pyfile('config.py')
app = Kobin(config=config)


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
