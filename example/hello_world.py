from kobin import Kobin, request, response

app = Kobin()


@app.route('^/favicon.ico$')
def favicon():
    with open('img/favicon.ico', 'rb') as f:
        image_data = f.read()
    return image_data


@app.route('^/$')
def index():
    return "Hello Kobin!"


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
