from kobin import Kobin, request, Response, JSONResponse

app = Kobin()


@app.route('/')
def hello() -> Response:
    print(request.headers)
    return Response("Hello World!!")


@app.route('/hello/{name}')
def hello(name: str) -> JSONResponse:
    return JSONResponse({
        "name": name
    })
