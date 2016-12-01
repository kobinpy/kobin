from kobin import Kobin

app = Kobin()


@app.route('/')
def hello() -> str:
    return "Hello World!!"


@app.route('/hello/{name}')
def hello(name: str) -> str:
    return "Hello {}!!".format(name)
