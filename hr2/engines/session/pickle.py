"""Session - session manager"""

class Session():
    name = "pickle"

    def __init__(self, pathname):
        self._pathname = pathname
        self._storage = {}

    def get(self, session_id, default=None):
        return self._storage.get(session_id, default)

    def delete(self, session_id):
        del self._storage[session_id]

    def set(self, session_id, value):
        self._storage[session_id] = value
