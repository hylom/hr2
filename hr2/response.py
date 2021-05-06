"""Request - HTTP(S) Response

   This module provides :class:`Response` class which represents HTTP response and retains HTTP response headers.

"""

__all__ = ["Response"]
__author__ = "Hiromichi Matsushima <hylom@hylom.net>"

import string
from http import HTTPStatus
import mimetypes
import os.path
import json

class Response():
    """This class represents HTTP response and retains HTTP response headers.
    """

    def __init__(self, router, start_response):
        self.start_response = start_response
        self._data = []
        self._status_code = None
        self.headers = []
        self.cookies = []
        self.router = router
        self._finished = False

    def __len__(self):
        """Returns size of response body.
        """
        size = 0
        for data in self._data:
            size += len(data)
        return size

    def add_cookie(self, cookie):
        """Add cookie to the response.

        :param cookie: cookie object to add the response
        :type cookie: cookie
        :return: self
        """
        self.cookies.append(cookie)
        return self

    def add_header(self, name, value):
        """Add response header to the response.

        :param string name: name of the header
        :param string value: value of the header
        :return: self
        """
        self.headers.append((name, value))
        return self

    def _start_response(self):
        for c in self.cookies:
            self.headers.append(c.to_header())

        status = HTTPStatus(self._status_code)
        status_str = "{} {}".format(status.value, status.phrase)
        self.start_response(status_str, self.headers)

    def __iter__(self):
        """Returns iterator for response body.
        """
        return iter(self._data)

    def end(self, data=None):
        """Close response.

        :param data: data to append the response body
        """
        if data:
            self._add_data(data)
        if not self._status_code:
            if self._data:
                self._status_code = 200
            else:
                self._status_code = 404
        self._finished = True

    def redirect(self, url, status_code=302):
        """Redirects to given URL.

        :param string url: URL to redirect
        :param status_code: status code
        :return: self
        """
        self._status_code = HTTPStatus(_status_code)
        self.headers = [('Location', url)]
        return self

    def _add_data(self, data):
        if not data:
            return
        if isinstance(data, str):
            self._data.append(data.encode())
        else:
            self._data.append(data)

    def status(self, status_code):
        """Set status code.

        :param int status_code: status code
        :return: self
        """
        self._status_code = status_code
        return self

    def get_status(self):
        """Get status code.

        :return: status code
        :rtype: int
        """
        return self._status_code

    def send_content(self, body=None, content_type=None):
        """Send contents.

        :param body: response body
        :param string content_type: content-type of the response body
        :return: self
        """
        if body:
            self._add_data(body)
        if content_type:
            self.headers.append(('Content-type', content_type))
        return self

    def send_json(self, data_dict):
        """Send contents as json.

        :param dict data_dict: data
        :return: self
        """
        data = json.dumps(data_dict, ensure_ascii=False)
        self.send_content(data, "application/json");
        return self

    def render(self, template, variables, content_type=None, engine=None):
        """Render template and send.

        :param string template: template
        :param dict variables: variables to use rendering
        :param string content_type: content-type
        :param string engine: engine name to use
        :return: self
        """
        renderer = self.router.renderer
        content = renderer.render(template, variables, content_type, engine)

        content_type = None
        if content["content_type"]:
            content_type = content["content_type"] + "; charset=utf-8"
        self.send_content(content["content"], content_type)
        return self

    def send_file(self, filepath):
        """Send static file.

        :param string filepath: filepath to send
        :return: self
        """
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

        self.send_content(content, mimetype)
        return self
