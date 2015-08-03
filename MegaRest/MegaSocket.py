# -*- coding: utf-8 -*-
__author__ = 'mvleandro'
import socket
import threading
import resource
import time


class MegaSocket(object):

    __connections = int()
    __queuee = list()

    def __init__(self, protocol, host='127.0.0.1', port=8017, connections=2000):
        self.__host = host
        self.__port = port
        self.__connections = connections
        self.__protocol = protocol
        self.__tcp = object

    def start(self):

        resource.setrlimit(resource.RLIMIT_NOFILE, (10000, 10000))

        self.__tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__tcp.bind((self.__host, self.__port))
        self.__tcp.listen(self.__connections)

        thread = threading.Thread(target=self.run_queuee)
        thread.start()

        while True:
            connection, client = self.__tcp.accept()
            while True:
                received_buffer = connection.recv(2048)
                if not received_buffer:
                    break

                self.__queuee.append((connection, client, received_buffer))
                #self.__protocol.run(connection, client, received_buffer)
                break

    def run_queuee(self):

        while True:

            if len(self.__queuee) > 0:
                args = self.__queuee.pop(0)
                self.__protocol.run(args[0], args[1], args[2])
            else:
                time.sleep(0.1)
