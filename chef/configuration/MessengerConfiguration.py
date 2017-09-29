import shelve

from chef.configuration.Configuration import Configuration
from chef.messagingdaemon import MessengerDaemon


class MessengerConfiguration(Configuration):

    def __init__(self, settings : shelve):
        MessengerDaemon.subscribe_to_channel(settings.get("messenger-thread-id"), self)
        super().__init__(settings)

    def send_message(self, message : str):
        MessengerDaemon.client.sendMessage(message, self.settings.get("messenger-thread-id"),
                                           self.settings.get("messenger-thread-type"))

    @staticmethod
    def get_configuration_type() -> str:
        return "messenger"
