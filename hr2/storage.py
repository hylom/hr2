"""storage - data storage class"""

class Storage():
    _results = []
    _in_transaction = False

    def __init__(self, engine, default_engine):
        self.storage = engine[default_engine]

    def get(self, key, default=None):
        try:
            r = self.storage[key]
        except KeyError:
            r = default
        if Storage._in_transaction:
            Storage._results.append(r)
        return r

    def clear(self):
        r = self.storage.clear()
        if Storage._in_transaction:
            Storage._results.append(r)
        return r

    def __getitem__(self, key):
        r = self.storage[key]
        if Storage._in_transaction:
            Storage._results.append(r)
        return r

    def __setitem__(self, key, value):
        self.storage[key] = value
        if Storage._in_transaction:
            Storage._results.append(None)

    def __delitem__(self, key):
        del self.storage[key]
        if Storage._in_transaction:
            Storage._results.append(None)

    def __enter__(self):
        if self.storage.has_transaction:
            return self.storage.__enter__()
        Storage._in_transaction = True
        Storage._results = []
        return self    

    def __exit__(self, exc_type, exc_value, traceback):
        if self.storage.has_transaction:
            return self.storage.__exit__(exc_type, exc_value, traceback)
        Storage._in_transaction = False
        return self    

    @property
    def results(self):
        if self.storage.has_transaction:
            return self.storage.results
        return Storage._results
