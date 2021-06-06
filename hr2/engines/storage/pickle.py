import pickle
import os
from .base import StorageBase

class Storage(StorageBase):
    name = "pickle"
    has_transaction = False
    
    def __init__(self, filepath):
        self.filepath = filepath
        self.storage = {}
        self.opened = False

    def _iter(self):
        if not self.opened:
            self.load()
        return iter(self.storage)

    def _get(self, key):
        if not self.opened:
            self.load()
        return self.storage[key]

    def _set(self, key, value):
        if not self.opened:
            self.load()
        self.storage[key] = value
        self.save()

    def _del(self, key):
        if not self.opened:
            self.load()
        del self.storage[key]
        self.save()

    def _clear(self):
        self.opened = False
        self.storage = {}
        try:
            os.unlink(self.filepath)
        except FileNotFoundError:
            pass

    def load(self):
        try:
            with open(self.filepath, 'rb') as fp:
                self.storage = pickle.load(fp)
            self.opened = True
        except:
            self.storage = {}
    
    def save(self):
        with open(self.filepath, 'wb') as fp:
            pickle.dump(self.storage, fp)
