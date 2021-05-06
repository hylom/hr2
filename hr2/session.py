"""Session - session manager"""

import uuid
from hr2.cookie import Cookie

class Session(dict):
    def __init__(self, engine, default_engine, req, res, config={}):
        self._data_store = engine[default_engine]
        self._cookie_name = 'session'
        self._cookie_path = '/'
        self._req = req
        self._res = res
        # acceptalbe params:
        params = {
            "Domain":   "domain",
            #"Path":     "path",
            "SameSite": "same_site",
            "Expires":  "expires",
            "HostOnly": "host_only",
            "HttpOnly": "http_only",
            "MaxAge":   "max_age",
            "Secure":   "secure",
        }
        self._config = {}
        for k in config:
            if k in params:
                self._config[params[k]] = config[k]
        
        #self._expiration = '3600'
        #self._domain = config["domain"]

    def _gen_cookie(self, value):
        return Cookie(name=self._cookie_name,
                      value=value,
                      path=self._cookie_path,
                      **self._config)

    def restore(self):
        self.clear()
        c = self._req.cookies.get(self._cookie_name, None)
        if c is None:
            self.update({})
            return
        self.restore_by_id(c.value)

    def restore_by_id(self, session_id):
        self.clear()
        try:
            value = self._data_store[session_id]
        except KeyError:
            value = {}
        self.update(value)

    def reset(self):
        self.clear()
        c = self._req.cookies.get(self._cookie_name, None)
        if c is None:
            return
        del self._data_store[c.value]

    def save(self):
        key = None
        c = self._req.cookies.get(self._cookie_name, None)
        if c is not None:
            key = c.value
            try:
                self._data_store[key]
            except KeyError:
                # session key is invalid,
                # so regenerate it
                key = None

        if key is None:
            key = uuid.uuid4().hex

        self._res.cookies.append(self._gen_cookie(key))
        self._data_store[key] = dict(self)
        return
