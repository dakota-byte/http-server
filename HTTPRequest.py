import os
import gzip
import config
from variables import *
from HTTPResponse import HTTPResponse


class HTTPRequest:
    def __init__(self, req):
        self.HTTP_METHOD = None
        self.REQUEST_TARGET = None
        self.HTTP_VERSION = None
        self.HEADERS = {}
        self.BODY = None
        self.fillRequest(req)

    # GET /index.html HTTP/1.1\r\nHost: localhost:4221\r\nUser-Agent: curl/7.64.1\r\nAccept: */*\r\n\r\n
    # GeT /index.html HTTP/1.1\r\nhost: localhost:4221\r\nUser-aGEnt :curl/7.64.1\r\nAccept: */*\r\n\r\n
    def fillRequest(self, req):
        sections = req.split("\r\n\r\n")
        body = sections[1] or ""
        lines = sections[0].split("\r\n")
        header = lines[0].split(" ")

        self.HTTP_METHOD = header[0]
        self.REQUEST_TARGET = header[1]
        self.HTTP_VERSION = header[2]

        for line in lines[1:]:
            if not line:  # \r\n\r\n creates empty lines
                continue
            parts = line.split(":")
            # we want to be case insensitive for headers, but still make sure to retain case in the values
            # when constructing our response we will still format things Like-This
            self.HEADERS[parts[0].lower().strip()] = parts[1].strip()

        self.BODY = body

        return self

    def getResponse(self):
        response = HTTPResponse()

        HTTP_METHOD = self.HTTP_METHOD.upper()
        REQUEST_TARGET = self.REQUEST_TARGET.lower()

        if HTTP_METHOD == "GET" and REQUEST_TARGET == "/":
            response.STATUS_LINE = HTTP_200

        if (HTTP_METHOD == "GET" or HTTP_METHOD == "HEAD") and REQUEST_TARGET.startswith("/echo/"):
            response.STATUS_LINE = HTTP_200
            response.addHeader("Content-Type", "text/plain")
            response.addHeader("Content-Length", len(self.REQUEST_TARGET) - 6)
            if HTTP_METHOD == "GET":
                response.setBody(self.REQUEST_TARGET[6:])

        if (HTTP_METHOD == "GET" or HTTP_METHOD == "HEAD") and REQUEST_TARGET == "/user-agent":
            user_agent = self.HEADERS["user-agent"]
            response.STATUS_LINE = HTTP_200
            response.addHeader("Content-Type", "text/plain")
            response.addHeader("Content-Length", len(user_agent))
            if HTTP_METHOD == "GET":
                response.setBody(user_agent)

        if (HTTP_METHOD == "GET" or HTTP_METHOD == "HEAD") and REQUEST_TARGET.startswith("/files/"):
            file_name = self.REQUEST_TARGET[7:]
            file_path = config.ServerConfig["directory"] + file_name
            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    file_contents = f.read()
                response.STATUS_LINE = HTTP_200
                response.addHeader("Content-Type", "application/octet-stream")
                response.addHeader("Content-Length", len(file_contents))
                if HTTP_METHOD == "GET":
                    response.setBody(file_contents)
            else:
                response.STATUS_LINE = HTTP_404

        if HTTP_METHOD == "POST" and self.REQUEST_TARGET.startswith("/files/"):
            file_name = self.REQUEST_TARGET[7:]
            file_path = config.ServerConfig["directory"] + file_name
            # We are also given Content-Type and Content-Length
            try:
                with open(file_path, "w") as f:
                    f.write(self.BODY)
                response.STATUS_LINE = HTTP_201
            except:
                response.STATUS_LINE = HTTP_404

        if "accept-encoding" in self.HEADERS:
            schemes = (
                self.HEADERS["accept-encoding"].replace(" ", "").split(",")
            )  # to avoid ", " vs ","
            selected_scheme = None
            for scheme in schemes:
                if scheme in config.ServerConfig["Content-Encoding"]:
                    selected_scheme = scheme
            if not selected_scheme:
                response.STATUS_LINE = HTTP_406
            if selected_scheme:
                response.addHeader("Content-Encoding", selected_scheme)

                current_body = response.RESPONSE_BODY
                cb_bytes = current_body.encode("utf-8")
                cb_compressed = gzip.compress(cb_bytes)

                response.setBody("")
                response.HEADERS["Content-Length"] = len(cb_compressed)

                response_encoded = response.createResponseString().encode("utf-8")
                response_encoded += cb_compressed

                return response_encoded

        return response.createResponseString().encode("utf-8")
