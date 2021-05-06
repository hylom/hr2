"""Handler - handler base class"""

class Handler():
    def __init__(self, app, req, res, status=None):
        self._app = app
        self._status = status
        self._req = req
        self._res = res
        self._session = None

        # build session
        self._session = self._app.get_session(req, res)
        if self._session != None:
            self._session.restore()

    def dispatch(self, req, res):
        self._app.log.debug("dispatch on {}".format(self))
        if hasattr(self, "request"):
            self.request(req, res)
            return

        if not req.method:
            res.status(500)
            return

        handler = getattr(self, req.method.lower(), None)
        if not handler:
            res.status(501)
            return

        handler(req, res)

    @property
    def app(self):
        return self._app

    @property
    def req(self):
        return self._req

    @property
    def res(self):
        return self._res

    @property
    def session(self):
        return self._session

    def get(self, req, res):
        status = self._status or 500
        res.render(status)

    def head(self, req, res):
        status = self._status or 500
        res.render(status)

