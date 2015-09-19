from kobin.routes import Router, Route


class Kobin(object):
    def __init__(self):
        self.router = Router()

    def run(self, host='', port=8000):
        try:
            from wsgiref.simple_server import make_server
            httpd = make_server(host, port, self)
            print('Serving on port %d...' % port)
            httpd.serve_forever()
        except KeyboardInterrupt:
            print('Goodbye.')

    def add_route(self, route):
        self.router.add(route.rule, route.method, route)

    def route(self, path=None, method='GET', callback=None):
        def decorator(callback_func):
            route = Route(self, path, method, callback_func)
            self.add_route(route)
            return callback_func
        return decorator(callback) if callback else decorator

    def _handle(self, environ):
        route, args = self.router.match(environ)
        return route.call()

    def wsgi(self, environ, start_response):
        out = self._handle(environ)
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [out]

    def __call__(self, environ, start_response):
        """It is called when receive http request."""
        return self.wsgi(environ, start_response)
