from typing import Callable, Dict, List
from .routes import Router, Route
from .server_adapters import servers
from .environs import request, response


class Kobin(object):
    def __init__(self) -> None:
        self.router = Router()

    def run(self, host: str='', port: int=8000, server: str='wsgiref', **kwargs):
        try:
            if server in servers:
                server = servers.get(server)
            if isinstance(server, type):
                server = server(host=host, port=port, **kwargs)

            print('Serving on port %d...' % port)
            server.run(self)  # type: ignore
        except KeyboardInterrupt:
            print('Goodbye.')

    def add_route(self, route: Route):
        self.router.add(route.rule, route.method, route)

    def route(self, path: str=None, method: str='GET',
              callback: Callable[..., str]=None) -> Callable[..., str]:
        def decorator(callback_func):
            route = Route(path, method, callback_func)
            self.add_route(route)
            return callback_func
        return decorator(callback) if callback else decorator

    def _handle(self, environ: Dict) -> str:
        route, kwargs = self.router.match(environ)
        environ['kobin.app'] = self
        request.bind(environ)  # type: ignore
        response.bind()        # type: ignore
        return route.call(**kwargs) if kwargs else route.call()

    def wsgi(self, environ: Dict, start_response) -> List[bytes]:
        out = self._handle(environ).encode('utf-8')  # type: bytes
        start_response(response._status_line, response.headerlist)
        return [out]

    def __call__(self, environ: Dict, start_response) -> List[str]:
        """It is called when receive http request."""
        return self.wsgi(environ, start_response)
