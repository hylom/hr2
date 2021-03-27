"""Handler - handler base class"""

class Handler():
    def __init__(self, app, status=None):
        self._app = app
        self._status = status

    def dispatch(self, req, res):
        self.req = req
        self.res = res

        if hasattr(self, "request"):
            self.request(req, res)
            return

        if not req.method:
            res.render(500)
            return

        handler = getattr(self, req.method.lower(), None)
        if not handler:
            res.render(501)
            return

        # build session
        if hasattr(self._app, 'session_class'):
            self.session = self._app.session_class(self._app, req, res)
            self.session.restore()

        handler(req, res)

    @property
    def app(self):
        return self._app

    def get(self, req, res):
        status = self._status or 500
        res.render(status)

    def head(self, req, res):
        status = self._status or 500
        res.render(status)

