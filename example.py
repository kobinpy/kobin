from kobin import Kobin, request

app = Kobin()


@app.route('^/favicon.ico$')
def favicon():
    with open('resources/favicon.ico', 'rb') as f:
        image_data = f.read()
    return image_data


@app.route('^/$')
def index():
    return "Hello Kobin!"


@app.route('^/user/(?P<name>\w+)/$')
def hello(name: str):
    return "Hello {}".format(name, request.path)

if __name__ == '__main__':
    app.run()
