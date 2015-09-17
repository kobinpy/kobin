
class HTTPError(Exception):
    def __init__(self, status, message, *args, **kwargs):
        print(status, message)
        super(HTTPError, self).__init__(*args, **kwargs)
