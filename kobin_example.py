from kobin import Kobin

app = Kobin()


@app.route('^/$')
def index():
    return "Hello Kobin!"


@app.route('^/user/(?P<name>\w+)/$')
def hello(name):
    return "Hello {}".format(name)

if __name__ == '__main__':
    app.run()

