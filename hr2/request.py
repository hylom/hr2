"""Request - HTTP(S) Request"""

from .cookie import Cookies
from .utils.query_param import QueryParameter

class Request():
    def __init__(self, router, environ):
        self.environ = environ
        self.router = router

    @property
    def method(self):
        return self.environ["REQUEST_METHOD"]

    @property
    def path(self):
        return self.environ["PATH_INFO"]

    @property
    def query(self):
        if not hasattr(self, "_query"):
            self._query = QueryParameter(self.environ["QUERY_STRING"])
        return self._query

    @property
    def raw_query(self):
        return self.environ["QUERY_STRING"]

    @property
    def protocol(self):
        return self.environ["SERVER_PROTOCOL"]

    @property
    def cookies(self):
        if not hasattr(self, "_cookies"):
            s = self.environ.get("HTTP_COOKIE", "")
            self._cookies = Cookies.from_header(s)
        return self._cookies

    @property
    def remote_address(self):
        return self.environ.get("REMOTE_ADDR")

    def header(self, name, default=None):
        var_name = "HTTP_" + name.upper()
        return self.environ.get(var_name, default)

