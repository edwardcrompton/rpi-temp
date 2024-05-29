from random import randrange
from datapointinterface import DatapointInterface

class Number(DatapointInterface):
    def get():
        return randrange(40)
