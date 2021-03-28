"""Session - session manager"""

import uuid
from hr2.cookie import Cookie

class Session(dict):
    def __init__(self, engine, default_engine, req, res):
        self._data_store = engine[default_engine]
        self._cookie_name = 'session'
        self._cookie_path = '/'
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
        self._data_store.delete(c.value)

    def save(self):
        c = self._req.cookies.get(self._cookie_name, None)
        if c is not None:
            key = c.value
            if not self._data_store.get(key):
                # session key is invalid,
                # so regenerate it
                c = None

        if c is None:
            key = uuid.uuid4().hex
            self._res.cookies.append(self._gen_cookie(key))

        self._data_store.set(key, dict(self))
        return
