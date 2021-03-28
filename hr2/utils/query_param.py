import urllib
#urllib.parse.parse_qs

class QueryParameter(dict):
    def __init__(self, query_string=None):
        if query_string:
            q = urllib.parse.parse_qs(query_string)
            self.update(q)

    def get_one(self, key, default=None):
        l = self.get(key, [])
        if l:
            return l[-1]
        return default
