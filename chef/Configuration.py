from chef.MessageParser import *
import abc
import shelve
from chef import DiscordBot







class Configuration(abc.ABC):

    def __init__(self, config : shelve):
        self.config = config

    @abc.abstractmethod
    async def send_message(self, message : str):
        raise NotImplementedError()

    async def receive_new_message(self, message : str):
        query = MessageParser.parse_message(message)
        response = query.apply(self)
        if response:
            await self.send_message(response)


class DiscordConfiguration(Configuration):

    def __init__(self, config : shelve):
        DiscordBot.listen_to_channel(config["discord-channel-id"], self)
        super().__init__(config)

    async def send_message(self, message : str):
        await DiscordBot.send_message(self.config["discord-channel-id"], message)



class ConfigurationCreator():

    @staticmethod
    def create_channel_from_config(config : shelve):
        if (config["configuration-type"] == "discord-channel"):
            return DiscordConfiguration(config)
        else:
            raise Exception("Invalid channel configuration")
