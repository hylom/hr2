import re
import os

class Config():
    def default(self):
        return self

    def __getitem__(self, key):
        env_key = self._camel_to_SNAKE(key)
        return os.environ[env_key]

    def _camel_to_SNAKE(self, key):
        key = re.sub(r'([^A-Z])([A-Z])', r'\1_\2', key)
        return key.upper()
