class Kobin(object):
    def wsgi(self, environ, start_response):
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [b'<b>Hello World from wsgi</b>']

    def __call__(self, environ, start_response):
        """It is called when receive http request."""
        return self.wsgi(environ, start_response)
