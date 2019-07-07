#!/usr/bin/env python

import argparse
import http.server
import os
import logging

class HTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
    def do_PUT(self):
        path = self.translate_path(self.path)
        if path.endswith('/'):
            self.send_response(405, "Method Not Allowed")
            self.wfile.write("PUT not allowed on a directory\n".encode())
            return
        else:
            try:
                os.makedirs(os.path.dirname(path))
            except FileExistsError: 
                pass
            length = int(self.headers['Content-Length'])
            with open(path, 'wb') as f:
                f.write(self.rfile.read(length))
            self.send_response(201, "Created")
            
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))
        print("\n" + post_data.decode('utf-8') + "\n")
            
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--bind', '-b', default='', metavar='ADDRESS',
                        help='Specify alternate bind address '
                             '[default: all interfaces]')
    parser.add_argument('port', action='store',
                        default=8080, type=int,
                        nargs='?',
                        help='Specify alternate port [default: 8080]')
    args = parser.parse_args()
    http.server.test(HandlerClass=HTTPRequestHandler, port=args.port, bind=args.bind)
