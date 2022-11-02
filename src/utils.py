class HeadersHandler:

    def parse(headers_):
        """Parse the headers from text to dictionary"""
        headers_ = headers_.split("\r\n")
        
        http = headers_[0].split()
        method, route, version = http

        builtin_routes = {
            "/": "/root",
            "favicon.ico": "/root"
        }

        route = method + builtin_routes.get(route, route)

        headers = {}
        headers.update({
            "method": method,
            "route": route,
            "version": version
        })

        for header in headers_:
            header = header.split(": ", 1)
            if (len(header) > 1):
                headers.update({header[0]: header[1]})

        return headers


class Request:
    def __init__(self, headers, body):
        self.headers = HeadersHandler.parse(headers)
        self.body = body


class Response:
    """Create a parsed response for browsers"""
    def __init__(self):
        self.version = "HTTP/1.1 "
        self.status = "200 OK\r\n"
        self.headers = {
            "Access-Control-Allow-Origin": "*",
            "Connection": "Keep-Alive",
            "Content-Type": "application/json; charset=utf-8"
        }
        self.body = ""

    def headers_str(self):
        headers = ""
        for key in self.headers:
            headers += key + ": " + self.headers[key] + "\r\n"
        return headers

    def encode(self):
        return bytes(
            self.version + self.status + self.headers_str() + "\r\n" + self.body,
            "ascii"
        )
