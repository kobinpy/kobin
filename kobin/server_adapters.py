from typing import Dict, Any

from . import Kobin


class ServerAdapter:
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


class GunicornServer(ServerAdapter):
    def run(self, handler: Kobin) -> None:
        from gunicorn.app.base import Application  # type: ignore

        config = {'bind': "{host}:{port}".format(host=self.host, port=self.port)}  # type: Dict[str, str]
        config.update(self.options)

        class GunicornApplication(Application):
            def init(self, parser, opts, args) -> Dict[str, str]:
                return config

            def load(self):
                return handler

        GunicornApplication().run()

servers = {
    'wsgiref': WSGIRefServer,
    'gunicorn': GunicornServer,
}  # type: Dict[str, Any]
