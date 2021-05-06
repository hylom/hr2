import re
import os

class Config():
    def __init__(self, section=None):
        self._section = section

    def default(self):
        return self

    def section(self, key):
        return Config(key)

    def __iter__(self):
        self._iter = iter(os.environ)
        return self

    def __next__(self):
        next_key = None
        while not next_key:
            next_key = self._SNAKE_to_camel(next(self._iter))
            if self._section:
                if next_key.find(self._section) == 0:
                    return next_key[len(self._section):]
                next_key = None
        return next_key

    def __getitem__(self, key):
        if not key:
            raise KeyError
        prefix = ""
        if self._section:
            prefix = self._camel_to_SNAKE(self._section) + "_"
        else:
            prefix = ""
        env_key = prefix + self._camel_to_SNAKE(key)
        return os.environ[env_key]

    def _camel_to_SNAKE(self, key):
        key = re.sub(r'([^A-Z])([A-Z])', r'\1_\2', key)
        return key.upper()

    def _SNAKE_to_camel(self, key):
        key = key.lower()
        key = re.sub(r'(_)([a-z])',
                     lambda m: m.group(2).upper(),
                     key)
        key = re.sub(r'^([a-z])',
                     lambda m: m.group(1).upper(),
                     key)
        return key
