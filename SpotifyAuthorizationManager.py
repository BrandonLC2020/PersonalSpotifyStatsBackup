from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse
import json

class GetHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        print('came in here to GET')
        parsed_path = urlparse(self.path)
        message = '\n'.join([
            'CLIENT VALUES:',
            'client_address=%s (%s)' % (self.client_address,
                self.address_string()),
            'command=%s' % self.command,
            'path=%s' % self.path,
            'real path=%s' % parsed_path.path,
            'query=%s' % parsed_path.query,
            'request_version=%s' % self.request_version,
            '',
            'SERVER VALUES:',
            'server_version=%s' % self.server_version,
            'sys_version=%s' % self.sys_version,
            'protocol_version=%s' % self.protocol_version,
            '',
            ])
        # self.send_response(200)
        # self.end_headers()
        print(self.path)
        return

    def do_POST(self):
        print('came in here to POST')        
        content_len = int(self.headers.getheader('content-length'))
        post_body = self.rfile.read(content_len)
        self.send_response(200)
        self.end_headers()

        data = json.loads(post_body)

        self.wfile.write(data['foo'])
        return

if __name__ == '__main__':
    from http.server import HTTPServer
    server = HTTPServer(('localhost', 3000), GetHandler)
    print('Starting server at http://localhost:3000')
    server.serve_forever()