from .base import StorageBase

class Storage(StorageBase):
    name = "inmemory"
    has_transaction = False
    
    def __init__(self):
        self.storage = {}

    def _iter(self):
        return iter(self.storage)

    def _get(self, key):
        return self.storage[key]

    def _set(self, key, value):
        self.storage[key] = value

    def _clear(self):
        self.storage = {}

    def _del(self, key):
        del self.storage[key]
