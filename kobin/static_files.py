from typing import Dict, List
import mimetypes  # type: ignore
import os
import time

from kobin.templates import load_file
from .environs import request, response


def static_file(filename: str,
                mimetype: str='auto',
                download: str='',
                charset: str='UTF-8') -> bytes:
    from . import current_config
    static_dirs = current_config()['STATICFILES_DIRS']  # type: List[str]
    filename = load_file(filename, static_dirs)  # Get abs path
    headers = dict()  # type: Dict[str, str]

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
        body = b''  # type: bytes
    else:
        with open(filename, 'rb') as f:
            body = f.read()

    headers["Accept-Ranges"] = "bytes"

    for k, v in headers.items():
        response.add_header(k, v)

    return body
