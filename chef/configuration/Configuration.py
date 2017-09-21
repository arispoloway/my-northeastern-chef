import shelve

from chef.MessageParser import *


class Configuration(abc.ABC):

    def __init__(self, settings : shelve):
        self.settings = settings

    @abc.abstractmethod
    def send_message(self, message : str):
        raise NotImplementedError()

    @staticmethod
    @abc.abstractmethod
    def get_configuration_type():
        raise NotImplementedError()

    def receive_new_message(self, message : str):
        query = MessageParser.parse_message(message)
        result = query.apply(self)
        return result


