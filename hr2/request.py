"""request - HTTP(S) Request related module

   This module provides :class:`Request` class which represents HTTP request and retains HTTP request headers.

"""

__all__ = ["Request"]
__author__ = "Hiromichi Matsushima <hylom@hylom.net>"

import json

from .cookie import Cookies
from .utils.query_param import QueryParameter


class Request():
    """This class represents HTTP request and retains HTTP request headers.
    """

    def __init__(self, router, environ):
        self._environ = environ
        self._router = router
        self._path = self.original_path

    @property
    def router(self):
        """This property holds router object associated the request.
        """
        return self._router

    # WSGI's defined variables
    @property
    def method(self):
        """This property holds HTTP method like ``GET``, ``POST``, ``PUT``, etc.
        """
        return self._environ["REQUEST_METHOD"]

    # SCRIPT_NAME: none

    @property
    def path(self):
        """This property holds request path. This value corresponds
            to ``PATH_INFO`` environment value of WSGI.
        """
        return self._path

    @path.setter
    def path(self, value):
        self._path = value

    @property
    def original_path(self):
        """This property holds original request path. This value corresponds
            to ``PATH_INFO`` environment value of WSGI.
        """
        return self._environ["PATH_INFO"]

    @property
    def query(self):
        """This property holds parsed querystring as hr2.utils.QueryParameter
           object. This parameter corresponds to ``QUERY_STRING``
           environment value of WSGI.
        """
        if not hasattr(self, "_query"):
            self._query = QueryParameter(self._environ["QUERY_STRING"])
        return self._query

    @property
    def content_type(self):
        """This property holds content type of the request.
           This parameter corresponds to ``CONTENT_TYPE``
           environment value of WSGI.
        """
        return self._environ["CONTENT_TYPE"]

    @property
    def content_length(self):
        """This property holds content length of the request.
           This parameter corresponds to ``CONTENT_LENGTH``
           environment value of WSGI.
        """
        return self._environ["CONTENT_LENGTH"]

    # SERVER_NAME
    # SERVER_PORT
    
    @property
    def raw_query(self):
        """This property holds raw query string value.
           This parameter corresponds to ``QUERY_STRING``
           environment value of WSGI.
        """
        return self._environ["QUERY_STRING"]

    @property
    def protocol(self):
        """This property holds protocol name of the request like ``HTTP/1.0``
           or ``HTTP/1.1``.
           This parameter corresponds to ``SERVER_PROTOCOL``
           environment value of WSGI.
        """
        return self._environ["SERVER_PROTOCOL"]

    @property
    def cookies(self):
        """This property holds cookies as hr2.cookie object.
           This object is created from to ``HTTP_COOKIE``
           environment value of WSGI.
        """
        if not hasattr(self, "_cookies"):
            s = self._environ.get("HTTP_COOKIE", "")
            self._cookies = Cookies.from_header(s)
        return self._cookies

    @property
    def remote_address(self):
        """This property holds remote (client's) IP address.
           This value corresponds to ``REMOTE_ADDR``
           environment value of WSGI.
        """
        return self._environ.get("REMOTE_ADDR")

    @property
    def json(self):
        """This property holds request body as Python dict.
           This property is valid only when content-type is ``application/json``.
           If content-type is not ``application/json``, raises
           :class:`hr2.Request.ContentTypeIsNotJson` exception.
        """
        if self.content_type != "application/json":
            raise this.ContentTypeIsNotJson(self.content_type)
        return json.loads(self.body)

    @property
    def body(self):
        """This property holds request body as `bytes`.
        """
        length = int(self._environ.get('CONTENT_LENGTH', 0))
        bytes_read = 0
        body = b""
        while bytes_read < length:
            b = self._input.read(length - bytes_read)
            bytes_read += len(b)
            body += b
        return body

    @property
    def _input(self):
        return self._environ.get("wsgi.input")
        
    def header(self, name, default=None):
        """This method returns value of the HTTP request header corresponds to
           given name. value of name parameter is case-insensitive.
        """
        var_name = "HTTP_" + name.replace("-", "_").upper()
        return self._environ.get(var_name, default)

    class ContentTypeIsNotJson(Exception):
        """This exception is raised when access Request.json property and the request's content-type is not ``application/json``.
        """
        pass
