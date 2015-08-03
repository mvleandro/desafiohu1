# -*- coding: utf-8 -*-
__author__ = 'mvleandro'
from MegaRest import *
from pymongo import MongoClient
import redis

HOST = '127.0.0.1'
PORT = 5000
CONNECTIONS = 3000

if __name__ == "__main__":

    mongoClient = MongoClient("mongodb://localhost:27017/")
    redis = redis.Redis("localhost")

    router = Router()
    router.add_route("/find", "app.control.HotelControl", "find")
    router.add_route("/availabilities", "app.control.HotelControl", "find_availability")

    rest = Rest(router, mongoClient, redis)

    server = MegaSocket(rest,HOST, PORT, CONNECTIONS)
    server.start()
