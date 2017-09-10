import abc

from chef.Channel import *


class Query(abc):

    @abc.abstractmethod
    def apply(self, channel : Channel) -> str:
        raise NotImplementedError("")



class InvalidQuery(Query):

    def __init__(self, message : str):
        self.message = message

    def apply(self, channel : Channel) -> str:
        return self.message


class ImmediateResponseQuery(Query):

    def apply(self, channel : Channel) -> str:
        #do this
        pass