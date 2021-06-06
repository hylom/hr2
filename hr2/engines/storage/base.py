import pickle

class StorageBase():
    has_transaction = True
    
    def __iter__(self):
        return self._iter()

    def __getitem__(self, key):
        return self._get(key)

    def __setitem__(self, key, value):
        return self._set(key, value)

    def __delitem__(self, key):
        return self._del(key)

    def clear(self):
        return self._clear()

    def __enter__(self):
        return self

    def __exit(self, exc_type, exc_value, traceback):
        pass


class SerializedStorageBase(StorageBase):
    def __getitem__(self, key):
        return self._deserialize(self._get(key))

    def __setitem__(self, key, value):
        return self._set(key, self._serialize(value))


class PickleStorageBase(SerializedStorageBase):
    def _serialize(self, obj):
        if obj is not None:
            return pickle.dumps(obj)
        return None

    def _deserialize(self, binary):
        if binary is not None:
            return pickle.loads(binary)
        return None

