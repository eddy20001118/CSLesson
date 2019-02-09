# -*- coding: utf-8 -*-
from http.server import BaseHTTPRequestHandler, HTTPServer
from pendulum import PendulumSim
from urllib.parse import urlparse, parse_qs
import json
import time

hostName = "localhost"
hostPort = 9000


class MyServer(BaseHTTPRequestHandler):
    sim = PendulumSim()
    ans = sim.run()

    def set_headers_json(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With,Content-Type")
        self.send_header("Access-Control-Allow-Methods","PUT,POST,GET,DELETE,OPTIONS")
        self.end_headers()

    def set_headers_html(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

    def do_GET(self):
        if (self.path == '/data'):
            response = {
                'status': 200,
                'type': 'calculation',
                'data': self.ans
            }
            self.set_headers_json()
            self.wfile.write(json.dumps(response).encode(
                encoding='utf_8', errors='strict'))
        elif (self.path == '/index.html'):
            response = {
                'status': 200,
                'data': 'index'
            }
            file = open('index.html','r',encoding='UTF-8')
            self.set_headers_html()
            self.wfile.write(file.read().encode(
                encoding='utf_8', errors='strict'))


myServer = HTTPServer((hostName, hostPort), MyServer)
print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))

try:
    myServer.serve_forever()
except KeyboardInterrupt:
    pass

myServer.server_close()
print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))
