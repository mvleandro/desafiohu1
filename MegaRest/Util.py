__author__ = 'mvleandro'
import time


class Util(object):

    @classmethod
    def date_to_epoch(cls, date, pattern):
        epoch = float(time.mktime(time.strptime(date, pattern)))
        return epoch
