"""access_log: access logger plugin"""

import time

class AccessLog():
    def __init__(self):
        pass

    def register(self, app):
        app.add_action('after_dispatch',  lambda req, res: self.log(req, res))

    def log(self, req, res):
        log_format = '{ip_addr} - {user} [{time}] "{method} {path} {protocol}" {status} {bytes} "{referer}" "{agent}"'
        time_format = "%d/%b/%Y:%H:%M:%S +0000"
        data = {
            "ip_addr": req.remote_address,
            "user": "-",
            "time": time.strftime(time_format, time.gmtime()),
            "method": req.method,
            "path": "?".join((req.path, req.raw_query)),
            "protocol": req.protocol,
            "status": res.status_code,
            "bytes": len(res),
            "referer": req.header('Referer',''),
            "agent": req.header('User-agent', ''),
        }
        log_str = log_format.format(**data)
        print(log_str)
