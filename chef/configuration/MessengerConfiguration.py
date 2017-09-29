import shelve

from chef import MessengerDaemon
from chef.configuration.Configuration import Configuration


class MessengerConfiguration(Configuration):

    def __init__(self, settings : shelve):


    def send_message(self, message : str):


    @staticmethod
    def get_configuration_type() -> str:
        return "messenger"