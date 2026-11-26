from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial
class Preview(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()
ThreadingHTTPServer(('127.0.0.1',4317),partial(Preview,directory='/Users/atharvawagh/Documents/Codex/2026-11-23/i-x20/ascend/dist')).serve_forever()
