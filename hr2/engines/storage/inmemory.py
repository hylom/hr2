class Storage():
    name = "inmemory"
    
    def __init__(self):
        self.storage = {}

    def __getitem__(self, key):
        return self.storage[key]

    def __setitem__(self, key, value):
        self.storage[key] = value

    def __delitem__(self, key):
        del self.storage[key]
