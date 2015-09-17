from kobin.app import Kobin

app = Kobin()


@app.route('/')
def hello():
    return b"Hello World"

if __name__ == '__main__':
    try:
        from wsgiref.simple_server import make_server
        httpd = make_server('', 8080, app)
        print('Serving on port 8080...')
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('Goodbye.')
