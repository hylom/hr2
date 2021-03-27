"""config - config helper class"""

import configparser
import re
import os

class IniConfig(configparser.ConfigParser):
    def __init__(self, app):
        super().__init__(self)
        self._app = app
        self.read("config.ini")

    def default(self):
        return self["default"]

class EnvVarConfig(dict):
    def __init__(self, app):
        self._app = app

    def default(self):
        return self

    def __getitem__(self, key):
        env_key = self._camel_to_SNAKE(key)
        return os.environ[env_key]

    def _camel_to_SNAKE(self, key):
        key = re.sub(r'([^A-Z])([A-Z])', r'\1_\2', key)
        return key.upper()
            

