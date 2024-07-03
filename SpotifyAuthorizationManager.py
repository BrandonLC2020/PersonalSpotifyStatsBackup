from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse
import json

class GetHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        print(self.path)
        if 'code=' in self.path and 'state=' in self.path:
            # get code and state
            print('went in here')
            return
        else:
            return

if __name__ == '__main__':
    from http.server import HTTPServer
    server = HTTPServer(('localhost', 3000), GetHandler)
    print('Starting server at http://localhost:3000')
    server.serve_forever()