"""config - config helper classes

   This module provides :class:`Config` class which contains application configuration values and provides to access them.

"""

__all__ = ["Config"]
__author__ = "Hiromichi Matsushima <hylom@hylom.net>"

class Config():
    """This class contains application configuration values and provides to access them.
    """
    def __init__(self, engine, default_engine):
        self._config = engine[default_engine]

    def __getitem__(self, key):
        return self._config.default()[key]

    def get(self, key, default=None):
        """Returns configuration value for given key.

        :param string key: key to access configuration value
        :param default: default value. default value is ``None``
        """
        try:
            return self._config.default()[key]
        except KeyError:
            return default

    def section(self, key):
        """Returns configuration subsection for given key.

        :param string key: key of subsection
        """
        return self._config.section(key)
