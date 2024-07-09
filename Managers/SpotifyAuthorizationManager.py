from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

class GetHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        print(self.path)
        if 'code=' in self.path and 'state=' in self.path:
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            code = query_params['code'][0]
            state = query_params['state'][0]
            data_message = code + ' ' + state
            f = open("authorization.txt", "x")
            f.write(data_message)
            return
        else:
            return

if __name__ == '__main__':
    from http.server import HTTPServer
    server = HTTPServer(('localhost', 3000), GetHandler)
    print('Starting server at http://localhost:3000')
    server.serve_forever()