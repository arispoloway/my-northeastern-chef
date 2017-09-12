from chef.MessageParser import *
import abc
import shelve
from chef import DiscordDaemon
import asyncio



class Configuration(abc.ABC):

    def __init__(self, settings : shelve):
        self.settings = settings

    @abc.abstractmethod
    def send_message(self, message : str):
        raise NotImplementedError()

    def receive_new_message(self, message : str):
        query = MessageParser.parse_message(message)
        result = query.apply(self)
        return result


class DiscordConfiguration(Configuration):
    configuration_type = "discord"

    def __init__(self, settings : shelve):
        DiscordDaemon.subscribe_to_channel(settings.get("discord-channel-id"), self)
        super().__init__(settings)

    def send_message(self, message : str):
        asyncio.run_coroutine_threadsafe(DiscordDaemon.send_message(self.settings.get("discord-channel-id"), message), DiscordDaemon.client.loop)



class ConfigurationCreator():

    @staticmethod
    def create_configuration_from_settings(settings : shelve):
        if (settings.get("configuration-type") == DiscordConfiguration.configuration_type):
            configuration = DiscordConfiguration(settings)
            ConfigurationCreationQuery().apply(configuration)
        else:
            raise Exception("Invalid channel configuration")
