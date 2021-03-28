"""Handler - handler base class"""

class Handler():
    def __init__(self, app, status=None):
        self._app = app
        self._status = status

    def dispatch(self, req, res):
        self.req = req
        self.res = res

        # build session
        self.session = self.app.get_session(req, res)
        if self.session != None:
            self.session.restore()

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

