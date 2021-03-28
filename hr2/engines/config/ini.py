"""ini - init config helper class"""

import configparser

class Config(configparser.ConfigParser):
    def __init__(self, path):
        super().__init__(self)
        self.read(path)

    def default(self):
        return self["default"]

            

