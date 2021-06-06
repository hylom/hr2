import redis
from .base import PickleStorageBase

class Storage(PickleStorageBase):
    name = "redis"

    def _connect(self):
        return redis.Redis(**self._opts)

    @property
    def redis(self):
        self.results = []
        if self._pipeline:
            return self._pipeline
        return self._connect()
    
    def __init__(self, config):
        self._opts = {}
        if "host" in config and config["host"]:
            self._opts["host"] = config["host"]
        if "port" in config and config["port"]:
            self._opts["port"] = config["port"]
        if "db" in config and config["db"] != "":
            self._opts["db"] = config["db"]
                
        self._prefix = config.get("prefix", "")
        self._pipeline = None
        self.results = []

    def _add_prefix(self, key):
        return self._prefix + ":" + key

    def _get(self, key):
        r = self.redis.get(self._add_prefix(key))
        if self._pipeline:
            return None
        if r is None:
            raise KeyError(key)
        return r

    def _set(self, key, value):
        r = self.redis.set(self._add_prefix(key), value)
        if self._pipeline:
            return None
        return r

    def _del(self, key):
        r = self.redis.delete(self._add_prefix(key))
        if self._pipeline:
            return None
        return r

    def clear(self):
        self.redis.flushdb()

    def __enter__(self):
        self._pipeline = self.redis.pipeline()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        def conv_results(r):
            if isinstance(r, bytes):
                return self._deserialize(r)
            return r
            
        self.results = [conv_results(x) for x in self._pipeline.execute()]
        self._pipeline = None
