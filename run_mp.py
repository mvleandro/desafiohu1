# -*- coding: utf-8 -*-
__author__ = 'mvleandro'

import socket
import multiprocessing
import resource
from MegaRest import *
from pymongo import MongoClient
import redis

HOST = '127.0.0.1'
PORT = 8000
MAX_CONCURRENT_JOBS = 100
CURRENT_RUNNING_JOBS = 0
CONNECTIONS = 3000


def handle_connection(connection, client):
    global CURRENT_RUNNING_JOBS

    message = connection.recv(2048)

    rest.run(connection,client,message)
    CURRENT_RUNNING_JOBS -= 1


if __name__ == "__main__":

    resource.setrlimit(resource.RLIMIT_NOFILE, (10000, 10000))

    mongoClient = MongoClient("mongodb://localhost:27017/")
    redis = redis.Redis("localhost")

    router = Router()
    router.add_route("/cities", "app.control.HotelControl", "find_cities")

    rest = Rest(router, mongoClient)

    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    orig = (HOST, PORT)

    tcp.bind(orig)
    tcp.listen(CONNECTIONS)

    while True:
        connection, client = tcp.accept()

        if CURRENT_RUNNING_JOBS < MAX_CONCURRENT_JOBS:
            process = multiprocessing.Process(target=handle_connection, args=tuple([connection, client]))
            CURRENT_RUNNING_JOBS += 1
            process.start()

    tcp.close()