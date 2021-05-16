"""static_file: plugin to serve static files"""

from hr2 import Handler
import time
import os.path

class StaticHandler(Handler):
    def get(self, req, res):
        if req.path[0] == "/":
            normpath = os.path.normpath(req.path[1:])
        else:
            normpath = os.path.normpath(req.path)
        if normpath == ".." or normpath[0:3] == "../":
            res.status(400)
            return
        root = os.path.abspath(self.root)
        pathname = os.path.join(root, normpath)
        self.app.log.debug("StaticHandler tries to serve %s for %s" % (pathname, req.original_path))
        if not os.path.isfile(pathname):
            res.status(404)
            return

        res.send_file(pathname)


class StaticFile():
    def __init__(self):
        pass

    def _rex_to_str(self, route):
        if route[0] == "^":
            route = route[1:]
        return route

    def register(self, app, kwargs={}):
        route = kwargs.get("route")
        router = kwargs.get("router", app)
        root = kwargs.get("root")
        options = kwargs.get("options", {})

        router.add_route(route, StaticHandler, replace="", root=root, options=options)
