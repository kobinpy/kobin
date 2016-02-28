from .environs import Response


class HTTPError(Response, Exception):
    default_status = 500

    def __init__(self, status: int, body: str,
                 exception: str=None, traceback: str=None, *args, **kwargs) -> None:
        super().__init__(status=status or self.default_status, body=body, *args, **kwargs)  # type: ignore
        self.exception = exception
        self.traceback = traceback
