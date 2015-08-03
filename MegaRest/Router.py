__author__ = 'mvleandro'


class Router(object):

    routes = list()

    def __init__(self):
        pass

    def add_route(self, path, class_name, method_name):
        route = {"path": path, "class_name": class_name, "method_name": method_name}
        self.routes.append(route)

    def get_route(self, path):
        for route in self.routes:
            if route["path"] == path:
                return route
        return False
