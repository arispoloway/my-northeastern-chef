from chef.MessageParser import *

class Channel(abc):

    def __init__(self):
        pass

    @abc.abstractmethod
    def send_message(self, message : str):
        raise NotImplementedError()

    def receive_new_message(self, message : str):
        query = MessageParser.parse_message(message)
        response = query.apply(self)
        if response:
            self.send_message(response)





