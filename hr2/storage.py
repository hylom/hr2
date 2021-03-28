"""storage - data storage class"""

class Storage():
    def __init__(self, engine, default_engine):
        self.storage = engine[default_engine]

    def get(self, key, default=None):
        try:
            return self.storage[key]
        except KeyError:
            return default

    def __getitem__(self, key):
        return self.storage[key]

    def __setitem__(self, key, value):
        self.storage[key] = value

    def __delitem__(self, key):
        del self.storage[key]

