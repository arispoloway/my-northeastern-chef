import abc

class Query(abc.ABC):

    @abc.abstractmethod
    def apply(self, channel ) -> str:
        raise NotImplementedError("")



class InvalidQuery(Query):

    def __init__(self, message):
        self.message = message

    def apply(self, channel) -> str:
        return self.message


class ImmediateResponseQuery(Query):

    def apply(self, channel) -> str:
        #do this
        pass