__author__ = 'mvleandro'
from MegaRest import IProtocol
import datetime
import urllib
import os


class Http(IProtocol.IProtocol):

    eol = "\n"

    request_data = dict()
    get = dict()
    post = dict()

    def __init__(self):
        super(Http,self).__init__()

    def __process_get(self):
        if len(self.request_data["query_string"]) > 0:
            if self.request_data["query_string"].count("&") > 0:
                query_string_parts = self.request_data["query_string"].split("&")
                for part in query_string_parts:
                    var_parts = part.split("=")
                    self.get[var_parts[0]] = urllib.unquote(var_parts[1])
            else:
                var_parts = self.request_data["query_string"].split("=")
                self.get[var_parts[0]] = urllib.unquote(var_parts[1])

    def __process_headers(self, headers):
        for header in headers:
            header_parts = header.split(":")

            if len(header_parts) > 1:
                if header_parts[0].lower() == "host":
                    self.request_data["server_name"] = header_parts[1]
                    if len(header_parts) > 2:
                        self.request_data["server_port"] = header_parts[2]
                        self.request_data["host"] = "%s:%s" % (header_parts[1], header_parts[2])
                    else:
                        self.request_data["host"] = header_parts[1]
                else:
                    self.request_data[header_parts[0].lower()] = str(header_parts[1]).strip()

    def request(self):

        self.request_data["remote_addr"] = self.client[0]
        self.request_data["remote_port"] = self.client[1]

        if self.data[-2:] == "\r\n":
            self.eol = "\r\n"
        else:
            self.eol = "\n"

        lines = list(self.data.split(self.eol))
        head = lines[0]
        del lines

        parts = head.split(" ")
        self.request_data["request_method"] = parts[0]
        self.request_data["request_uri"] = parts[1]
        self.request_data["request_protocol"] = parts[2]

        if self.request_data["request_uri"].count("?") > 0:
            request_uri_parts = self.request_data["request_uri"].split("?")
            self.request_data["request_path"] = request_uri_parts[0]
            self.request_data["query_string"] = request_uri_parts[1]
        else:
            self.request_data["request_path"] = self.request_data["request_uri"]
            self.request_data["query_string"] = ''

        self.__process_get()
        #TODO Processar dados POST

        headers = list(self.data.split(self.eol))[1:-2]
        self.__process_headers(headers)

        self.action = self.request_data["request_path"]

    def reply(self):
        self.log()

    def http_reponse(self, status, message, content_type, data=""):

        headers = []
        now = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')

        headers.append("HTTP/1.1 %s %s" % (status, message))
        headers.append("Date: %s" % now)
        headers.append("Server: MegaRest 0.1 Beta")
        headers.append("Content-Type: %s" % content_type)
        headers.append("Access-Control-Allow-Origin: *")

        if len(data) > 0:
            headers.append("Content-Length: %s" % str(len(data)))

        headers.append("Expires: Sat, 01 Jan 2000 00:59:59 GMT")
        headers.append("Last-Modified: Fri, 09 Aug 1996 14:21:40 GMT")

        headers_str = self.eol.join(headers)

        response = headers_str + (self.eol*2) + data
        return response

    def log(self, _str = ""):
        log_file = open("access.log", "a")

        now = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
        default = "%s %s %s" % (now, self.request_data["request_method"], self.request_data["request_uri"])

        message = default + " " + _str + "\n"

        log_file.write(message)
        log_file.close()
