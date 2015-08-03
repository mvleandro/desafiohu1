__author__ = 'mvleandro'
from abc import ABCMeta, abstractmethod


class IProtocol:

    __metaclass__ = ABCMeta

    action = ''
    data = ''
    client = tuple()
    connection = object()

    @abstractmethod
    def request(self):
        pass

    @abstractmethod
    def reply(self):
        pass

    @abstractmethod
    def log(self):
        pass

    def __init__(self):
        super(IProtocol,self).__init__();

    def config(self, connection, client, buffer_data):
        self.data = buffer_data
        self.client = client
        self.connection = connection

    def run(self, connection, client, buffer_data):

        self.data = buffer_data
        self.client = client
        self.connection = connection

        self.request()
        self.reply()
        #self.connection.close()