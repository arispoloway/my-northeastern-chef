import shelve

from chef import DiscordDaemon
from chef.configuration.Configuration import Configuration


class DiscordConfiguration(Configuration):

    def __init__(self, settings : shelve):
        DiscordDaemon.subscribe_to_channel(settings.get("discord-channel-id"), self)
        super().__init__(settings)

    def send_message(self, message : str):
        DiscordDaemon.send_message(self.settings.get("discord-channel-id"), message)

    @staticmethod
    def get_configuration_type():
        return "discord"