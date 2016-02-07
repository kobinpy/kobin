class ServerAdapter(object):
    quiet = False

    def __init__(self, host='127.0.0.1', port=8080, **options):
        self.options = options
        self.host = host
        self.port = int(port)

    def run(self, handler):
        pass

    def __repr__(self):
        args = ', '.join(['%s=%s' % (k, repr(v))
                          for k, v in self.options.items()])


class WSGIRefServer(ServerAdapter):
    def run(self, app):
        from wsgiref.simple_server import make_server
        self.httpd = make_server(self.host, self.port, app)
        self.port = self.httpd.server_port

        try:
            self.httpd.serve_forever()
        except KeyboardInterrupt:
            self.httpd.server_close()
            raise

servers = {
    'wsgiref': WSGIRefServer,
}
