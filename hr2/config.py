"""config - config helper class"""


class Config():
    def __init__(self, engine, default_engine):
        self._config = engine[default_engine]

    def __getitem__(self, key):
        return self._config.default()[key]
