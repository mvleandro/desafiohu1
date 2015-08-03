__author__ = 'mvleandro'

class Hotel(object):

    def __init__(self, id, name, city):
        self.__id = id
        self.__name = name
        self.__city = city

    
    @property
    def id(self):
        return self.__id
    
    @property
    def name(self):
        return self.__name
        
    @property
    def city(self):
        return self.__city
    
    @id.setter
    def id(self,value):
        self.__id = value
        
    @name.setter
    def name(self,value):
        self.__name = value
        
    @city.setter
    def city(self,value):
        self.__city = value