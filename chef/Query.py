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


class NextOccurrenceQuery(Query):

    def __init__(self, food, location="", time=""):
        self.food = food
        self.location = location
        self.time = time


    def apply(self, configuration) -> str:
        configuration.send_message("Next " + self.food + ", " + self.location + ", " + self.time)



class CurrentStatusQuery(Query):

    def __init__(self, food, dining_hall="", time=""):
        self.food = food
        self.dining_hall = dining_hall
        self.time = time

    def apply(self, configuration) -> str:
        raise NotImplementedError()


