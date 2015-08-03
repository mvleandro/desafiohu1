__author__ = 'mvleandro'

from pymongo import MongoClient
from datetime import datetime

mongoClient = MongoClient("mongodb://localhost:27017/")
db = mongoClient.desafio

hoteisCollection = db.hotels
disponibilidadeCollection = db.availability

print "Limpando a base..."
hoteisCollection.delete_many({})
disponibilidadeCollection.delete_many({})

hoteisFileData = open("../assets/hoteis.txt","r")

print "Populando hoteis..."
for line in hoteisFileData.readlines():
    hotelSplit = line.split(',')
    hotelData = {
        "id": int(hotelSplit[0]),
        "city": hotelSplit[1],
        "name": hotelSplit[2][:-2]
    }
    post_id = hoteisCollection.insert_one(hotelData).inserted_id
    print "Incluido registro %s -> %s - %s" % (post_id,hotelData["city"], hotelData["name"])

hoteisFileData.close()
print "hoteis 100% populado"

disponibilidadeFileData = open("../assets/disp.txt","r")

print "Populando disponibilidade..."
for line in disponibilidadeFileData.readlines():
    dispSplit = line.split(',')
    dispData = {
        "hotel_id": int(dispSplit[0]),
        "hotel_obj": hoteisCollection.find_one({"id": int(dispSplit[0])})["_id"],
        "hotel": hoteisCollection.find_one({"id": int(dispSplit[0])}),
        "date": datetime.strptime(dispSplit[1], "%d/%m/%Y"),
        "available": (int(dispSplit[2][:-1])==1)
    }
    post_id = disponibilidadeCollection.insert_one(dispData).inserted_id
    print "Incluido registro %s -> %s - %s" % (post_id,dispData["date"], dispData["available"])

disponibilidadeFileData.close()
print "disponibilidade 100% populado"
