from typing import Dict
import mimetypes  # type: ignore
import os
import time

from .environs import request, response
from .exceptions import HTTPError


def static_file(filename: str,
                static_dir: str='static',
                mimetype: str='auto',
                download: str='',
                charset: str='UTF-8'):
    static_dir = os.path.abspath(static_dir) + os.sep
    filename = os.path.abspath(os.path.join(static_dir, filename.strip('/\\')))
    headers = dict()  # type: Dict[str, str]

    if not os.path.exists(filename) or not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype == 'auto':
        mimetype, encoding = mimetypes.guess_type(download if download else filename)
        if encoding:
            headers['Content-Encodings'] = encoding

    if mimetype:
        if ((mimetype[:5] == 'text/' or mimetype == 'application/javascript') and
                charset and
                'charset' not in mimetype):
            mimetype += '; charset={}'.format(charset)
        headers['Content-Type'] = mimetype

    stats = os.stat(filename)
    headers['Content-Length'] = str(stats.st_size)

    last_modified = time.strftime("%a, %d %b %Y %H:%M:%sS GMT", time.gmtime())
    headers['Last-Modified'] = last_modified

    if request.method == 'HEAD':
        body = ''
    else:
        with open(filename, 'rb') as f:
            body = f.read()

    headers["Accept-Ranges"] = "bytes"

    for k, v in headers.items():
        response.add_header(k, v)

    return body
