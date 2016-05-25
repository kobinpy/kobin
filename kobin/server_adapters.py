from typing import Dict, Any

from .app import Kobin


class ServerAdapter:
    quiet = False  # type: bool

    def __init__(self, host: str, port: int, **options) -> None:
        self.options = options
        self.host = host
        self.port = int(port)

    def run(self, handler: Kobin):
        raise NotImplementedError

    def __repr__(self):
        args = ', '.join(['{key}={value}'.format(key=k, value=repr(v))
                          for k, v in self.options.items()])
        return "{class}(args)".format(self.__class__.__name__, args)


class WSGIRefServer(ServerAdapter):
    def run(self, app: Kobin) -> None:
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

            def load(self) -> Kobin:
                return handler

        GunicornApplication().run()

servers = {  # type: Dict[str, Any]
    'wsgiref': WSGIRefServer,
    'gunicorn': GunicornServer,
}
