import json

class Storage():
    name = "json"
    
    def __init__(self, filepath):
        self.filepath = filepath
        self.storage = {}
        self.opened = False

    def __getitem__(self, key):
        if not self.opened:
            self.load()
        return self.storage[key]

    def __setitem__(self, key, value):
        self.storage[key] = value
        self.save()

    def __delitem__(self, key):
        del self.storage[key]
        self.save()

    def load(self):
        with open(self.filepath, 'r') as fp:
            self.storage = json.load(fp)
        self.opened = True
    
    def save(self):
        with open(self.filepath, 'w') as fp:
            json.dump(self.storage, fp)
