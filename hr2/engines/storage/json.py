import json
import os
from .base import StorageBase

class Storage(StorageBase):
    name = "json"
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
        self.storage[key] = value
        self.save()

    def _del(self, key):
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
            with open(self.filepath, 'r') as fp:
                self.storage = json.load(fp)
        except FileNotFoundError:
            self.storage = {}
        self.opened = True
    
    def save(self):
        with open(self.filepath, 'w') as fp:
            json.dump(self.storage, fp)
