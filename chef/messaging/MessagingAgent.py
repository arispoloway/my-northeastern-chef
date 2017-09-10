import abc

class NewMessageListener(abc):

    def receive_new_message(self, message : str):
        raise NotImplementedError("")


class MessagingAgent(abc):

    def __init__(self, listener : NewMessageListener = None):
        self.listeners = []
        if listener:
            self.listeners.append(listener)

    def send_message(self, message : str):
        raise NotImplementedError("")

    def add_new_message_listener(self, listener : NewMessageListener):
        self.listeners.append(listener)

    def notify_new_message_listeners(self, message : str):
        for listener in self.listeners:
            listener.receive_new_message(message)




