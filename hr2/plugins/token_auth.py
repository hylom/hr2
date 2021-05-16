"""token based authentification plugin"""

class TokenAuth():
    def register(self, app, args={}):
        self._app = app
        self._token_header = args["token_header"]
        if not self._token_header:
            self.app.log.error("TokenAuth: no token_header given!")
            
        app.add_action('before_dispatch',
                       lambda handler, req, res: self.token_auth(req, res))

    @property
    def app(self):
        return self._app

    def action_for_token(self, token, req, res):
        self.app.log.error("TokenAuth: you have to override action_for_token()!")

    def token_auth(self, req, res):
        token = req.header(self._token_header)
        self.action_for_token(token, req, res)
