"""Cookie - HTTP cookie"""

import re
import urllib

class InvalidCookieNameError(Exception):
    def __init__(self, name):
        self._name = name

class Cookies(list):
    def from_header(header):
        if len(header) == 0:
            return Cookies([])
        items = [re.split(r'=', x) for x in re.split(r';\s+', header)]
        d = [Cookie(x[0], x[1]) for x in items]
        return Cookies(d)

    def get(self, name, default=None):
        for c in self:
            if c.name == name:
                return c
        return default

class Cookie():
    def __init__(self, name, value, domain=None, path=None, same_site=None,
                 expires=None, host_only=None, http_only=None,
                 max_age=None, secure = None):
        self.name = name
        self.value = value
        self.domain = domain
        self.path = path
        self.same_site = same_site
        self.expires = expires
        self.host_only = host_only
        self.http_only = http_only
        self.max_age = max_age
        self.secure = secure

    def to_header(self):
        return ("Set-Cookie", str(self))

    def __str__(self):
        items = []
        if re.search(r'[,;" ]', self.name):
            raise InvalidCookieNameError(name=name)

        if self.value is None:
            v = ""
        else:
            v = self.value

        items.append("{}={}".format(self.name, urllib.parse.quote(v)))

        if self.expires is not None:
            date_str = dt.strftime("%a, %d %b %Y %H:%M:%S %Z")
            items.append("Expires={}".format(date_str))
        if self.domain is not None:
            items.append("Domain={}".format(self.domain))
        if self.path is not None:
            items.append("Path={}".format(self.path))
        if self.secure is not None:
            items.append("Secure")
        if self.http_only is not None:
            items.append("HttpOnly")
        if self.same_site is not None:
            items.append("SameSite={}".format(self.same_site))
        if self.max_age is not None:
            items.append("Max-Age={}".format(self.max_age))

        return "; ".join(items)
                        
    def to_string(self):
        pass

