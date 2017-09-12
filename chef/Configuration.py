from chef.MessageParser import *
import abc
import shelve
from chef import DiscordDaemon



class Configuration(abc.ABC):

    def __init__(self, settings : shelve):
        self.settings = settings

    @abc.abstractmethod
    async def send_message(self, message : str):
        raise NotImplementedError()

    async def receive_new_message(self, message : str):
        query = MessageParser.parse_message(message)
        response = query.apply(self)
        if response:
            await self.send_message(response)


class DiscordConfiguration(Configuration):

    def __init__(self, settings : shelve):
        DiscordDaemon.subscribe_to_channel(settings["discord-channel-id"], self)
        super().__init__(settings)

    async def send_message(self, message : str):
        await DiscordDaemon.send_message(self.settings["discord-channel-id"], message)



class ConfigurationCreator():

    @staticmethod
    def create_configuration_from_settings(settings : shelve):
        if (settings["configuration-type"] == "discord-channel"):
            return DiscordConfiguration(settings)
        else:
            raise Exception("Invalid channel configuration")
