from kobin import Kobin

app = Kobin()


@app.route('^/$')
def hello():
    return "Hello World"


@app.route('^/hoge/(?P<year>[0-9]{4})/$')
def hello(year):
    return "Hello {}".format(year)

if __name__ == '__main__':
    app.run()
