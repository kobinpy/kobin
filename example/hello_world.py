from kobin import Kobin

app = Kobin()


@app.route('^/(?P<name>\w*)$')
def hello(name: str) -> str:
    return "Hello {}!!".format(name)

if __name__ == '__main__':
    app.run()
