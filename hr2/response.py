"""Request - HTTP(S) Response"""

import string
from http import HTTPStatus
import mimetypes
import os.path

class Response():
    def __init__(self, router, start_response):
        self.start_response = start_response
        self._data = []
        self.headers = []
        self.cookies = []
        self.router = router

    def __len__(self):
        size = 0
        for data in self._data:
            size += len(data)
        return size

    def end(self, data=None):
        self._add_data(data)

    def add_cookie(self, cookie):
        self.cookies.append(cookie)

    def _start_response(self):
        for c in self.cookies:
            self.headers.append(c.to_header())

        status = HTTPStatus(self.status_code)
        status_str = "{} {}".format(status.value, status.phrase)
        self.start_response(status_str, self.headers)

    def __iter__(self):
        return iter(self._data)

    def redirect(self, url, status_code=302):
        self.status_code = HTTPStatus(status_code)
        self.headers = [('Location', url)]

    def _add_data(self, data):
        if not data:
            return
        if isinstance(data, str):
            self._data.append(data.encode())
        else:
            self._data.append(data)
    
    def render(self, status=None, body=None):
        if not status and body:
            status = 200
        self.status_code = status
        if body:
            self._add_data(body)
        else:
            st = HTTPStatus(status)
            self._add_data(st.phrase)

    def renderTemplate(self, template, variables,
                       status_code=200, content_type=None, engine=None):
        renderer = self.router.renderer
        content = renderer.render(template, variables, content_type, engine)

        content_type = None
        if content["content_type"]:
            content_type = content["content_type"] + "; charset=utf-8"
        self.status_code = status_code
        if content_type:
            self.headers.append(('Content-type', content_type))
        self._add_data(content["content"])

    def renderFile(self, filepath, status_code=200):
        (mimetype, enc)  = mimetypes.guess_type(filepath)
        mode = "rb"

        if mimetype.find("text") == 0:
            mode = "r"
            mimetype = mimetype + "; charset=utf-8"

        abspath = os.path.join(self.router.root_dir, filepath)
        with open(abspath, mode) as fp:
            content = fp.read()

        if mode == "r":
            content = content.encode()

        self.status_code = status_code
        self.headers.append(('Content-type', mimetype))
        self._add_data(content)
