"""router - define Router class"""

import re
import os.path

from .handler import Handler
from .request import Request
from .response import Response

from .template import Template
from .config import Config
from .session import Session
from .storage import Storage
from .logger import Logger

from .engines.template import string as string_template
from .engines.session import inmemory
from .engines.config import env_var

class InvalidActionTrigger(Exception):
    pass

class FaviconHandler(Handler):
    def get(self, req, res):
        res.renderFile("resources/favicon/favicon.ico")

class Router():
    def make_handler(self):
        return lambda environ, start_response: self.handler(environ, start_response)

    def handler(self, environ, start_response):
        path = environ["PATH_INFO"]
        handler = self.get_handler_for_path(path)

        if not handler:
            handler = Handler(self, status=404)

        req = Request(self, environ)
        res = Response(self, start_response)

        handler.dispatch(req, res)

        for action in self._after_dispatch_actions:
            action(req, res)

        res._start_response()
        return iter(res)
        
    def __init__(self):
        self.routes = []
        self.template_dirs = []
        self.log = Logger()

        # predefined engines
        self.default_engine = {
            "template": "string_template",
            "session": "inmemory",
            "config": "env_var",
        }
        self.engine = {
            "template": {
                "string_template": string_template.Renderer(),
            },
            "session": {
                "inmemory": inmemory.Session(),
            },
            "config": {
                "env_var": env_var.Config(),
            },
        }

        self._after_dispatch_actions = []
        self.add_route(r'^/favicon.ico$', FaviconHandler)


        self.startup()

        if not self.template_dirs:
            d = os.path.join(self.root_dir, "templates")
            self.log.debug("set template dir: {}".format(d))
            self.template_dirs = [d]

    @property
    def config(self):
        return Config(self.engine['config'],
                      self.get_default_engine("config"))

    @property
    def storage(self):
        return Storage(self.engine['storage'],
                       self.get_default_engine("storage"))

    @property
    def renderer(self):
        return Template(self.engine['template'],
                        self.template_dirs,
                        self.get_default_engine("template"))

    def get_session(self, req, res):
        return Session(self.engine['session'],
                       self.get_default_engine("session"),
                       req, res)

    def startup(self):
        pass

    def get_default_engine(self, engine_type):
        return self.default_engine.get(engine_type, None)

    def set_default_engine(self, engine_type, name):
        self.log.debug("set default engine for {}: {}".format(engine_type, name))
        self.default_engine[engine_type] = name

    def add_engine(self, engine_type, engine):
        self.log.debug("add engine for {}: {}".format(engine_type, engine.name))
        if not self.engine.get(engine_type):
            self.engine[engine_type] = {}
        self.engine[engine_type][engine.name] = engine

    def add_engine_as_default(self, engine_type, engine):
        self.add_engine(engine_type, engine)
        self.set_default_engine(engine_type, engine.name)

    def add_action(self, trigger, handler):
        if trigger == "after_dispatch":
            self._after_dispatch_actions.append(handler)
            return
        raise InvalidActionTrigger

    def add_plugin(self, plugin_class):
        self.log.debug("add plugin: {}".format(plugin_class))
        plugin_class().register(self)

    def add_route(self, rex, handler):
        self.log.debug("add route for {}: {}".format(rex, handler))
        self.routes.append((rex, handler))

    def get_handler_for_path(self, path):
        for (p, h_class) in self.routes:
            if re.search(p, path):
                return h_class(self)
        return None

