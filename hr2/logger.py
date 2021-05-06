import sys
import os
from datetime import datetime

LOG_LEVEL = {
    "debug": 10,
    "info": 20,
    "warn": 30,
    "error": 40,
    "fatal": 50,
}

class Logger():
    def __init__(self):
        self._verbosity = 40 # default value
        debug_level = os.environ.get("DEBUG")
        if debug_level:
            if debug_level.lower() in LOG_LEVEL:
                self._verbosity = LOG_LEVEL[debug_level.lower()]
            else:
                try:
                    self._verbosity = int(debug_level)
                except ValueError as e:
                    raise self.InvalidLogLevel(debug_level) from e

    def set_level(self, level):
        if isinstance(level, int):
            self._verbosity = level
            return
        lv = LOG_LEVEL.get(level)
        if level is None:
            raise self.InvalidLogLevel(level)
        self._verbosity = lv

    def log(self, log_level, *args):
        if log_level < self._verbosity:
            return
        ts = "[%s]" % datetime.now().isoformat()
        print(ts, *args, file=sys.stderr)

    def debug(self, *args):
        self.log(10, "[debug]", *args)

    def info(self, *args):
        self.log(20, "[info]", *args)

    def warn(self, *args):
        self.log(30, "[warn]", *args)

    def error(self, *args):
        self.log(40, "[error]", *args)

    def fatal(self, *args):
        self.log(50, "[fatal]", *args)

    class InvalidLogLevel(Exception):
        pass
