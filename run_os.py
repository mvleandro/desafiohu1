# -*- coding: utf-8 -*-
__author__ = 'mvleandro'

import socket
import os
import sys
import resource
from MegaRest import *
from pymongo import MongoClient
import redis


HOST = '127.0.0.1'
PORT = 1200
MAX_CONCURRENT_JOBS = 3
CURRENT_RUNNING_JOBS = 0
CONNECTIONS = 3000


if __name__ == "__main__":

    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    orig = (HOST, PORT)
    tcp.bind(orig)
    tcp.listen(CONNECTIONS)

    resource.setrlimit(resource.RLIMIT_NOFILE, (10000, 10000))

    mongoClient = MongoClient("mongodb://localhost:27017/")
    redis = redis.Redis("localhost")

    router = Router()
    router.add_route("/cities", "app.control.HotelControl", "find_cities")

    rest = Rest(router, mongoClient)

    while True:

        connection, client = tcp.accept()

        if CURRENT_RUNNING_JOBS < MAX_CONCURRENT_JOBS:
            pid = os.fork()
            CURRENT_RUNNING_JOBS += 1

            if pid == 0:
                tcp.close()
                while True:
                    msg = connection.recv(2048)
                    if not msg: break

                    rest.run(connection,client,msg)
                    CURRENT_RUNNING_JOBS -=1
                    sys.exit(0)

            else:
                connection.close()