import abc

class Query(abc.ABC):

    @abc.abstractmethod
    def apply(self, configuration) -> str:
        raise NotImplementedError("")


class ConfigurationCreationQuery(Query):
    def __init__(self):
        pass

    def apply(self, configuration):
        configuration.send_message("Successfully enabled food notification bot!")

class InvalidQuery(Query):

    def __init__(self, message):
        self.message = message

    def apply(self, configuration) -> str:
        if self.message:
            configuration.send_message(self.message)


class ImmediateResponseQuery(Query):

    def apply(self, configuration) -> str:
        #do this
        pass