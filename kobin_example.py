from kobin import Kobin

app = Kobin()


@app.route('/')
def hello():
    return b"Hello World"


@app.route('/hoge')
def hello():
    return b"Hello HOGEHOGE"

if __name__ == '__main__':
    app.run()
