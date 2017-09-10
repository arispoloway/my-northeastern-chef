from chef.Query import *



class MessageParser(object):

    @staticmethod
    def parse_message(message : str) -> Query:
        if "!bot" not in message:
            return InvalidQuery("")
        return InvalidQuery("Nothing is implemented yet")
