
class HTTPError(Exception):
    def __init__(self, status: int, message: str, *args, **kwargs) -> None:
        print(status, message)
        super().__init__(*args, **kwargs)
