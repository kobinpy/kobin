from typing import Dict, Any


class ServerAdapter(object):
    quiet = False

    def __init__(self, host: str='127.0.0.1', port: int=8080, **options) -> None:
        self.options = options
        self.host = host
        self.port = int(port)

    def run(self, handler):
        pass

    def __repr__(self):
        args = ', '.join(['%s=%s' % (k, repr(v))
                          for k, v in self.options.items()])
        return "%s(%s)" % (self.__class__.__name__, args)


class WSGIRefServer(ServerAdapter):
    def run(self, app):
        from wsgiref.simple_server import make_server  # type: ignore
        self.httpd = make_server(self.host, self.port, app)
        self.port = self.httpd.server_port

        try:
            self.httpd.serve_forever()
        except KeyboardInterrupt:
            self.httpd.server_close()
            raise

servers = {
    'wsgiref': WSGIRefServer,
}  # type: Dict[str, Any]
