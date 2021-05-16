import re

TRIGGERS = [
    "after_dispatch",
    "before_dispatch",
]

class SubRouter():
    def __init__(self, app):
        self._app = app
        # routes format is: (rex, handler, method, replace, kwargs)
        self._routes = []
        self._actions = {}
        pass

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

    def _run_action(self, trigger, handler, req, res):
        if trigger not in TRIGGERS:
            raise InvalidActionTrigger
        for action in self._actions.get(trigger, []):
            action(handler, req, res)

    def add_route(self, rex, handler, method=None, replace=None, **kwargs):
        self._routes.append((rex, handler, method, replace, kwargs))

    def new_sub_router(self, rex, replace='/'):
        r = SubRouter(self._app)
        self._routes.append((rex, r, None, replace, {}))
        return r

    def _get_handler_for_path(self, path, req_verb):
        for (p, handler, method, replace, kwargs) in self._routes:
            if method and method != req_verb:
                continue
            if re.search(p, path):
                if replace is not None:
                    new_path = re.sub(p, replace, path)
                else:
                    new_path = None
                return handler, new_path, kwargs
        return None, None, None

    def _apply_args(self, handler, kwargs):
        for k in kwargs:
            setattr(handler, k, kwargs[k])
    
    def dispatch(self, req, res):
        handler, new_path, kwargs = self._get_handler_for_path(req.path, req.method)
        if not handler:
            return

        if type(handler) == type(object):
            handler = handler(self._app, req, res)
            self._apply_args(handler, kwargs)
        if new_path:
            req.path = new_path

        self._app.log.debug("dipatch to {}: {} {}".format(handler, req.method, req.path))

        self._run_action("before_dispatch", handler, req, res)
        handler.dispatch(req, res)
        self._run_action("after_dispatch", handler, req, res)
