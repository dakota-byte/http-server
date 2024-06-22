from variables import *


class HTTPResponse:
    def __init__(self):
        self.STATUS_LINE = HTTP_404  # default, if all else fails
        self.HEADERS = {}
        self.RESPONSE_BODY = None

    class HTTPResponseError(Exception):
        pass

    def createResponseString(self):
        if not self.STATUS_LINE:
            raise self.HTTPResponseError("HTTPResponse Error: STATUS_LINE Required")

        response_str = ""
        response_str += self.STATUS_LINE
        response_str += "\r\n"

        for header, value in self.HEADERS.items():
            response_str += str(header) + ": " + str(value) + "\r\n"

        response_str += "\r\n"

        if self.RESPONSE_BODY:
            response_str += self.RESPONSE_BODY

        return response_str

    def addHeader(self, key, value):
        self.HEADERS[key] = value

    def setBody(self, body):
        self.RESPONSE_BODY = body
