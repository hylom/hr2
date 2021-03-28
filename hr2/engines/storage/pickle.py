import pickle

class Storage():
    name = "pickle"
    
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
        try:
            with open(self.filepath, 'rb') as fp:
                self.storage = pickle.load(fp)
            self.opened = True
        except:
            self.storage = {}
    
    def save(self):
        with open(self.filepath, 'wb') as fp:
            pickle.dump(self.storage, fp)
