__author__ = 'mvleandro'
import re
import json
import datetime
import base64
from MegaRest import Util


class HotelControl(object):

    def __init__(self):
        pass

    @classmethod
    def find(cls, protocol):


        if dict(protocol.get).has_key("query"):

            key = base64.b64encode("query: " + protocol.get["query"].lower().strip())
            cached = protocol.cachedb.get(key)

            if cached:

                json_decoder = json.JSONDecoder()
                json_response = json_decoder.decode(cached)

                return json_response
            else:

                str_regex = ".*%s.*" % str(protocol.get["query"]).lower()
                regex = re.compile(str_regex, re.IGNORECASE)

                response = []
                for hotel in protocol.db.hotels.find( { "$or": [ { "city": regex}, {"name": regex } ] }, {"_id": 0}).distinct("city"):
                    response.append(hotel)

                json_encoder = json.JSONEncoder()
                json_data = json_encoder.encode(response)

                protocol.cachedb.set(key, json_data)
                protocol.cachedb.expire(key, 60)

                return response

        else:
            raise Exception("Missing URL argument query")

    @classmethod
    def find_availability(cls, protocol):


        if dict(protocol.get).has_key("city"):
            city = protocol.get["city"].strip()

            if dict(protocol.get).has_key("no_date_range"):
                no_date_range = (int(protocol.get["no_date_range"].strip()) == 1)
            else:
                no_date_range = False

            if not no_date_range:

                if (not dict(protocol.get).has_key("checkin_date")) or (not dict(protocol.get).has_key("checkout_date")):
                    raise Exception("You must informe checkin and checkout date")

                checkin_date = protocol.get["checkin_date"].strip()
                checkout_date = protocol.get["checkout_date"].strip()

                checkin_date = Util.date_to_epoch(checkin_date, "%d/%m/%Y")
                checkout_date = Util.date_to_epoch(checkout_date, "%d/%m/%Y")

                key = city + str(checkin_date) + str(checkout_date)
            else:
                key = city

            key = base64.b64encode("search: " + str(key))

            cached = protocol.cachedb.get(key)

            if cached:

                json_decoder = json.JSONDecoder()
                json_response = json_decoder.decode(cached)

                return json_response
            else:

                if no_date_range:
                    pipeline = [
                        {"$match": {"hotel.city": city, "available": True}},
                        {"$sort": {"hotel.name": -1}},
                        {"$project": {"hotel_id": 1, "hotel.name": 1, "hotel.city": 1, "available": 1}},
                        {"$group": {"_id": { "hotel_id": "$hotel_id", "date": "$date", "city": "$hotel.city", "name": "$hotel.name", "available": "$available" }}},
                    ]

                else:
                    pipeline = [
                        {"$match": {
                            "hotel.city": city,
                            "available": True,
                            "date": {
                                "$gte": datetime.datetime.utcfromtimestamp(checkin_date),
                                "$lte": datetime.datetime.utcfromtimestamp(checkout_date)
                            }
                        }},
                        {"$sort": {"hotel.name": -1}},
                        {"$project": {"hotel_id": 1, "hotel.name": 1, "hotel.city": 1, "available": 1}},
                        {"$group": {"_id": { "hotel_id": "$hotel_id", "date": "$date", "city": "$hotel.city", "name": "$hotel.name", "available": "$available" }}},
                    ]

                response = []
                for availability in protocol.db.availability.aggregate(pipeline):
                    item = {
                        "city": availability["_id"]["city"],
                        "hotel": availability["_id"]["name"],
                        "hotel_id": availability["_id"]["hotel_id"],
                        "available": availability["_id"]["available"]
                    }
                    response.append(item)

                json_encoder = json.JSONEncoder()
                json_data = json_encoder.encode(response)

                protocol.cachedb.set(key, json_data)
                protocol.cachedb.expire(key, 60)

                return response

        else:
            raise Exception("You must choose your city")