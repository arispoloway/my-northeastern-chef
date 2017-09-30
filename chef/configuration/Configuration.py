import shelve

from chef.MessageParser import *


class Configuration(abc.ABC):

    def __init__(self, settings : shelve):
        self.settings = settings

    @abc.abstractmethod
    def send_message(self, message : str):
        raise NotImplementedError()

    def get_database(self):
        return FoodDatabaseSelector.get_school_database(self.settings.get("school"))

    @staticmethod
    @abc.abstractmethod
    def get_configuration_type() -> str:
        raise NotImplementedError()

    def receive_new_message(self, message : str):
        query = MessageParser.parse_message(message)
        result = query.apply(self)
        return result


