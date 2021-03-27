"""Session - session manager"""

import uuid
from .cookie import Cookie

DATA_STORE = {}

class InMemorySession(dict):
    def __init__(self, app, req, res):
        self._data_store = DATA_STORE
        self._cookie_name = 'session'
        self._cookie_path = '/'
        self._app = app
        self._req = req
        self._res = res
        #self._expiration = '3600'
        #self._domain = config["domain"]

    def _gen_cookie(self, value):
        return Cookie(name=self._cookie_name,
                      value=value,
                      path=self._cookie_path)

    def restore(self):
        self.clear()
        c = self._req.cookies.get(self._cookie_name, None)
        if c is None:
            return
        self.update(self._data_store.get(c.value, {}))

    def reset(self):
        self.clear()
        c = self._req.cookies.get(self._cookie_name, None)
        if c is None:
            return
        if c.value in self._data_store:
            del self._data_store[c.value]

    def save(self):
        c = self._req.cookies.get(self._cookie_name, None)
        if c is not None:
            key = c.value
            if key not in self._data_store:
                # session key is invalid,
                # so regenerate it
                c = None

        if c is None:
            key = uuid.uuid4().hex
            self._res.cookies.append(self._gen_cookie(key))

        self._data_store[key] = dict(self)
        return
