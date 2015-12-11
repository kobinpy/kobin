from kobin import Kobin

app = Kobin()


@app.route('^/$')
def hello():
    return "Hello World"


@app.route('^/user/(?P<name>\w+)/$')
def hello(name):
    return "Hello {}".format(name)

if __name__ == '__main__':
    app.run()
