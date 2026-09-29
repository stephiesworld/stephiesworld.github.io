#!/usr/bin/env python3
"""Local preview server that never lets the browser cache, so a plain refresh shows the latest edits."""
import http.server, sys

class NoCache(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()

port = int(sys.argv[1]) if len(sys.argv) > 1 else 3456
http.server.ThreadingHTTPServer(('', port), NoCache).serve_forever()
