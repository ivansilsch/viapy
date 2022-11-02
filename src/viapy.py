from socketserver import TCPServer, ThreadingMixIn, StreamRequestHandler
from utils import Request, Response
import json
import os


class RequestHandler(StreamRequestHandler):
    
    def handle(self):
        data = str(self.request.recv(4096), "ascii")
        data = data.split("\r\n\r\n", 1)

        headers = data[0]
        body = data[1]
        request = Request(headers, body)
        response = Response()

        request_route = request.headers["route"]
        request_route = "root" if request_route == "/" else request_route.replace("/", "_")
        route_parts = request_route.split("_")

        available_routes = [r for r in dir(self.router) if not r.startswith("__") ]
        for av_route in available_routes:
            av_route_parts = av_route.split("_")

            same_method = route_parts[0] == av_route_parts[0]
            same_root = route_parts[1] == av_route_parts[1]

            if len(route_parts) == len(av_route_parts) and same_method and same_root:
                print(route_parts, av_route_parts)
                route = getattr(self.router, av_route)
                response.body = json.dumps(route())
                break
                 
        self.request.sendall(response.encode())


class ThreadedTCPServer(ThreadingMixIn, TCPServer):
    allow_reuse_address = True


class App:

    def __init__(self):
        self.router = None
        self.RoutedRequestHandler = None

    def config(self, router):
        RoutedRequestHandler = type("RequestHandler", (RequestHandler,), {
            "router": router
        })
        self.RoutedRequestHandler = RoutedRequestHandler

    def run(self, host="127.0.0.1", port=5000):
        self.server = ThreadedTCPServer((host, port), self.RoutedRequestHandler)

        with self.server:
            ip, port = self.server.server_address
            print("Listening on {}:{}".format(ip, port))
            self.server.serve_forever()
            # self.server.shutdown()
