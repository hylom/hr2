"""router - define Router class"""

import re
import os.path

from .handler import Handler
from .request import Request
from .response import Response
from .engines.template import string as string_template
from .template import Template

class InvalidActionTrigger(Exception):
    pass

class FaviconHandler(Handler):
    def get(self, req, res):
        res.renderFile("resources/favicon/favicon.ico")

class Router():
    def __init__(self, environ, start_response):
        self.environ = environ
        self.start_response = start_response
        self.routes = []
        self.template_dirs = []
        self.default_template_engine = None

        # string engine is always enabled 
        self.engine = {
            "template": {
                "template": string_template.Renderer(),
                "string": string_template.Renderer(),
            },
        }

        self._after_dispatch_actions = []
        self.add_route(r'^/favicon.ico$', FaviconHandler)

        self.startup()
        self.cfg = self.config_class(self)

    @property
    def config(self):
        return self.cfg.default()

    def startup(self):
        pass

    def get_template_renderer(self):
        return Template(self.engine['template'],
                        self.template_dirs,
                        self.default_template_engine)

    def add_action(self, trigger, handler):
        if trigger == "after_dispatch":
            self._after_dispatch_actions.append(handler)
            return
        raise InvalidActionTrigger

    def add_plugin(self, plugin_class):
        plugin_class().register(self)

    def add_route(self, rex, handler):
        self.routes.append((rex, handler))

    def add_engine(self, engine_type, name, engine):
        if not self.engine.get(engine_type):
            self.engine[engine_type] = {}
        self.engine[engine_type][name] = engine

    def get_handler_for_path(self, path):
        for (p, h_class) in self.routes:
            if re.search(p, path):
                return h_class(self)
        return None

    def __iter__(self):
        path = self.environ["PATH_INFO"]
        handler = self.get_handler_for_path(path)

        if not handler:
            handler = Handler(self, status=404)

        req = Request(self, self.environ)
        res = Response(self, self.start_response)

        handler.dispatch(req, res)

        for action in self._after_dispatch_actions:
            action(req, res)

        res._start_response()
        return iter(res)
        
