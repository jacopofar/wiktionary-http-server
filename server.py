#!/usr/bin/env python3
import http.server
import json
import sqlite3
from urllib.parse import urlparse, unquote

PORT = 8090
CURSOR = sqlite3.connect("file:dict.db?mode=ro", uri=True).cursor()

class WiktHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        path_parts = urlparse(self.path).path.split('/')
        # expect /w/someword
        # the /w/ is for future API extensions
        assert path_parts[1] == 'w'
        word = unquote(path_parts[2])
        print(f'Looking for word {word}')
        entries = CURSOR.execute(
            "SELECT entries from words where word = ?", (word,)
        ).fetchone()

        status = 404
        response = None

        if entries is None:
            status = 404
            response = json.dumps(dict(error=f"cannot find {word}")).encode()
        else:
            status = 200
            response= entries[0].encode()
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(response)

if __name__ == '__main__':
    server = http.server.HTTPServer(('localhost', PORT), WiktHandler)
    print(f'Wiktionary server started on port {PORT}')
    server.serve_forever()
