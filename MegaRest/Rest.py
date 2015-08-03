__author__ = 'mvleandro'
from MegaRest import Http
from MegaRest import Router
import json


class Rest(Http):
    __router = Router()
    __not_found = False
    __server_error = False
    db = object()
    cachedb = object()

    def __init__(self, router, db_connection, cachedb_connection):
        super(Rest,self).__init__()
        self.__router = router
        self.__method = getattr(self, "dummy")
        self.db = db_connection.desafio
        self.cachedb = cachedb_connection

    def dummy(self):
        pass

    def request(self):
        super(Rest, self).request()

        route = self.__router.get_route(self.action)
        if route is not False:
            self.__method = self.__load_method(route)
            self.__not_found = False
        else:
            self.__not_found = True

    def reply(self):

        if self.__not_found is False:

            try:
                response = self.__method(self)

                json_encoder = json.JSONEncoder()
                json_response = json_encoder.encode(response)

                server_response = self.http_reponse("200", "OK", "application/json; charset=utf-8", json_response)
                self.connection.send(server_response)
            except Exception, e:
                server_response = self.http_reponse("500", "Internal Server Error", "text/html; charset=utf-8")
                server_response += "<h1>%s</h1>" % e.message
                self.connection.send(server_response)

        else:

            server_response = self.http_reponse("404", "Page Not Found", "text/html; charset=utf-8")
            server_response += "<h1>404 - Page Not Found</h1>"
            self.connection.send(server_response)

        super(Rest, self).reply()


    def my_import(self, name):
        mod = __import__(name)
        components = name.split('.')
        for comp in components[1:]:
            mod = getattr(mod, comp)
        return getattr(mod,comp)

    def __load_method(self, route):

        controller = self.my_import(route["class_name"])
        return getattr(controller, route["method_name"], False)

