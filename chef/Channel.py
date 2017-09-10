from chef.MessageParser import *
from chef.messaging.MessagingAgent import *


class Channel(NewMessageListener):

    def __init__(self):
        self.messaging_agent = None

    def set_messaging_agent(self, agent : MessagingAgent):
        agent.add_new_message_listener(self)
        self.messaging_agent = agent

    def send_message(self, message : str):
        self.messaging_agent.send_message(message)

    def receive_new_message(self, message : str):
        query = MessageParser.parse_message(message)
        response = query.apply(self)
        if response:
            self.send_message(response)





