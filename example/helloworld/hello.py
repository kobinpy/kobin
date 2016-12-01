from kobin import Kobin, Response, JSONResponse

app = Kobin()


@app.route('/')
def hello() -> Response:
    return Response("Hello World!!")


@app.route('/hello/{name}')
def hello(name: str) -> JSONResponse:
    return JSONResponse({
        "name": name
    })
