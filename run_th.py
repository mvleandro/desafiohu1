# -*- coding: utf-8 -*-
__author__ = 'mvleandro'

import socket
import thread
import resource
from MegaRest import *
from pymongo import MongoClient
import redis

HOST = '127.0.0.1'
PORT = 2000
MAX_CONCURRENT_JOBS = 4
CURRENT_RUNNING_JOBS = 0
CONNECTIONS = 3000


def handle_connection(connection, client):
    global CURRENT_RUNNING_JOBS

    while True:
        message = connection.recv(2048)
        if not message: break

        rest.run(connection,client,message)
        CURRENT_RUNNING_JOBS -= 1
        break

    connection.close()
    thread.exit()


if __name__ == "__main__":

    try:

        print "Iniciando servidor na porta %s" % str(PORT)

        resource.setrlimit(resource.RLIMIT_NOFILE, (10000, 10000))

        mongoClient = MongoClient("mongodb://localhost:27017/")
        redis = redis.Redis("localhost")

        router = Router()
        router.add_route("/find", "app.control.HotelControl", "find")
        router.add_route("/availabilities", "app.control.HotelControl", "find_availability")

        rest = Rest(router, mongoClient, redis)

        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        orig = (HOST, PORT)

        tcp.bind(orig)
        tcp.listen(CONNECTIONS)

        while True:

            if CURRENT_RUNNING_JOBS < MAX_CONCURRENT_JOBS:
                connection, client = tcp.accept()
                thread.start_new_thread(handle_connection, tuple([connection, client]))
                CURRENT_RUNNING_JOBS += 1

        tcp.close()
    except Exception, e:
        print "Erro ao iniciar o servidor"
