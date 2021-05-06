import unittest
from webtest import TestApp
from hr2.should import It

# TestApp uses TestResponse.
# see: https://docs.pylonsproject.org/projects/webtest/en/2.0/testresponse.html

class RouterTestCase(unittest.TestCase):
    def __init__(self, methodName='runTest'):
        super().__init__(methodName)

    def setRouter(self, app):
        self._app = TestApp(app.make_handler())

    def get(self, path_info, headers=[]):
        resp = self._app.get(path_info, headers=headers, status='*')
        return It(resp, self)

    def options(self, path_info, headers=[]):
        resp = self._app.options(path_info, headers=headers, status='*')
        return It(resp, self)

    def delete(self, path_info, headers=[]):
        resp = self._app.delete(path_info, headers=headers, status='*')
        return It(resp, self)

    def post(self, path_info, json=None, headers=[]):
        if json:
            resp = self._app.post_json(path_info, json,
                                       headers=headers, status='*')
        return It(resp, self)
