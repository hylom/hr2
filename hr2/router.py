"""Router - HTTP(S) Router

   This module provides :class:`Router` class which represents HTTP router.

"""

__all__ = ["Router"]
__author__ = "Hiromichi Matsushima <hylom@hylom.net>"

import re
import os.path
import inspect
from pathlib import Path

from .handler import Handler
from .request import Request
from .response import Response
from .subrouter import SubRouter

from .template import Template
from .config import Config
from .session import Session
from .storage import Storage
from .logger import Logger

from .engines.template import string as string_template
from .engines.storage import inmemory
from .engines.config import env_var

class FaviconHandler(Handler):
    """This class provides Favicon handler.
    """
    def get(self, req, res):
        res.send_file("resources/favicon/favicon.ico")

TRIGGERS = [
    "after_dispatch",
    "before_dispatch",
]

class Router(SubRouter):
    """This class provieds HTTP(S) router.
    """
    def __init__(self):
        super().__init__(self)
        self.template_dirs = []
        self.log = Logger()
        self._actions = {}

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
                "inmemory": inmemory.Storage(),
            },
            "config": {
                "env_var": env_var.Config(),
            },
        }

        self.add_route(r'^/favicon.ico$', FaviconHandler)


        self.startup()

        if not self.template_dirs:
            d = os.path.join(self.root_dir, "templates")
            self.log.debug("set template dir: {}".format(d))
            self.template_dirs = [d]

    def make_handler(self):
        """Returns WSGI handler function.
        """
        return lambda environ, start_response: self._app_dispatch(environ, start_response)

    def _app_dispatch(self, environ, start_response):
        #print("%s: receive request" % environ["PATH_INFO"])
        path = environ["PATH_INFO"]
        req = Request(self, environ)
        res = Response(self, start_response)

        self._run_action("before_dispatch", req, res)
        self.dispatch(req, res)
        self._run_action("after_dispatch", req, res)

        if not res._finished:
            res.end()

        res._start_response()
        #print("%s: start response" % environ["PATH_INFO"])
        return iter(res)
        
    @property
    def config(self):
        """This property holds defualt config object.
        """
        return Config(self.engine['config'],
                      self.get_default_engine("config"))

    @property
    def storage(self):
        """This property holds defualt storage object.
        """
        return Storage(self.engine['storage'],
                       self.get_default_engine("storage"))

    @property
    def renderer(self):
        """This property holds defualt renderer object.
        """
        return Template(self.engine['template'],
                        self.template_dirs,
                        self.get_default_engine("template"))

    @property
    def base_path(self):
        """This property holds directory which the main module in.
        """
        return Path(inspect.getfile(self.__class__)).parent

    def get_session(self, req, res):
        """Returns current session.

        :param Request req: current request object
        :param Response res: current response object
        :return: current session object
        """
        return Session(self.engine['session'],
                       self.get_default_engine("session"),
                       req, res, self.config.section("Session"))

    def startup(self):
        """This is Virtual function. Extended class can override this
        to execute their own initalize routine.
        """
        pass

    def get_default_engine(self, engine_type):
        """Returns default engine for given type

        :param string engine_type: engine type
        """
        return self.default_engine.get(engine_type, None)

    def set_default_engine(self, engine_type, name):
        """Set default engine for given type

        :param string engine_type: engine type
        :param string name: engine name to use as default engine
        """
        self.log.debug("set default engine for {}: {}".format(engine_type, name))
        self.default_engine[engine_type] = name

    def add_engine(self, engine_type, engine):
        """Add given type engine
        
        :param string engine_type: engine type
        :param engine: engine to add
        """
        self.log.debug("add engine for {}: {}".format(engine_type, engine.name))
        if not self.engine.get(engine_type):
            self.engine[engine_type] = {}
        self.engine[engine_type][engine.name] = engine

    def add_engine_as_default(self, engine_type, engine):
        """Add given type engine as default engine
        
        :param string engine_type: engine type
        :param engine: engine to add
        """
        self.add_engine(engine_type, engine)
        self.set_default_engine(engine_type, engine.name)

    def add_action(self, trigger, handler):
        """Add action handler for given trigger
        
        :param string trigger: trigger to add handler
        :param handler: handler to add
        """
        if trigger not in TRIGGERS:
            raise InvalidActionTrigger
        handlers = self._actions.get(trigger)
        if handlers:
            handlers.append(handler)
        else:
            self._actions[trigger] = [handler,]

    def _run_action(self, trigger, req, res):
        if trigger not in TRIGGERS:
            raise InvalidActionTrigger
        for action in self._actions.get(trigger, []):
            action(req, res)
        

    def add_plugin(self, plugin_class, **kwargs):
        """Add plugin
        
        :param class plagin_class: plagin class
        :param kwargs: kwargs to give plugin
        """
        self.log.debug("add plugin: {}".format(plugin_class))
        plugin_class().register(self, kwargs)

    class InvalidActionTrigger(Exception):
        """This exception is raised when add_action() is called
        and given trigger is not registered.
        """
        pass



