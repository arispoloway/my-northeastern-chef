import shelve

from chef.MessageParser import *
from chef.database.NeuFoodDatabase import db_user


class Configuration(abc.ABC):

    def __init__(self, settings : shelve):
        self.settings = settings

    @abc.abstractmethod
    def send_message(self, message : str):
        raise NotImplementedError()


    def get_database(self):
        return db_user()   # in the future this should use self.settings to determine which database

    @staticmethod
    @abc.abstractmethod
    def get_configuration_type() -> str:
        raise NotImplementedError()

    def receive_new_message(self, message : str):
        query = MessageParser.parse_message(message)
        result = query.apply(self)
        return result


