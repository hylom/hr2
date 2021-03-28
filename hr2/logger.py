import sys

LOG_LEVEL = {
    "debug": 10,
    "info": 20,
    "warn": 30,
    "error": 40,
    "fatal": 50,
}

class Logger():
    def __init__(self):
        self.verbosity = 10

    def log(self, log_level, *args):
        if log_level < self.verbosity:
            return
        print(*args, file=sys.stderr)

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

        
