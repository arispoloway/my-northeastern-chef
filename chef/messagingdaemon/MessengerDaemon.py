from fbchat import log, Client

from chef.configuration.ConfigurationCreator import ConfigurationCreator
from chef.configuration.ConfigurationSettings import ConfigurationSettings
from chef.configuration.MessengerConfiguration import MessengerConfiguration

client = None

callbacks = {}

# Subclass fbchat.Client and override required methods
class MessengerBot(Client):
    def onMessage(self, author_id, message, thread_id, thread_type, **kwargs):
        if thread_id in callbacks:
            callbacks[thread_id].receive_new_message(message)
        else:
            if message.startswith("!register"):
                configuration_settings = ConfigurationSettings.create_new_settings(MessengerConfiguration.get_configuration_type(), thread_id)
                configuration_settings.set("messenger-thread-id", thread_id)
                configuration_settings.set("messenger-thread-type", thread_type)
                ConfigurationCreator.create_configuration_from_settings(configuration_settings)

        self.markAsDelivered(author_id, thread_id)
        self.markAsRead(author_id)

        log.info("Message from {} in {} ({}): {}".format(author_id, thread_id, thread_type.name, message))

def subscribe_to_channel(thread : str, callback : MessengerConfiguration):
    callbacks[thread] = callback

def start_messenger_daemon(email : str, password : str):
    global client
    client = MessengerBot(email, password)
    client.listen()
