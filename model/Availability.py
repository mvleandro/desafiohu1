__author__ = 'mvleandro'

class Availability(object):

    def __init__(self, hotel, date, available):
        self.__hotel = hotel
        self.__date = date
        self.__available = available


    @property
    def hotel(self):
        return self.__hotel

    @property
    def date(self):
        return self.__date

    @property
    def available(self):
        return self.__available

    @hotel.setter
    def hotel(self,hotel):
        self.__hotel = hotel

    @date.setter
    def date(self, date):
        self.__date = date

    @available.setter
    def available(self,available):
        self.__available = available