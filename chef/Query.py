import abc



class Query(abc.ABC):

    @abc.abstractmethod
    def apply(self, configuration):
        raise NotImplementedError("")


class ConfigurationCreationQuery(Query):
    def __init__(self):
        pass

    def apply(self, configuration):
        configuration.send_message("Successfully enabled food notification bot!")


class InvalidQuery(Query):

    def __init__(self, message):
        self.message = message

    def apply(self, configuration):
        if self.message:
            configuration.send_message(self.message)


class NextOccurrenceQuery(Query):

    def __init__(self, food, location="", time=""):
        self.food = food
        self.location = location
        self.time = time


    def apply(self, configuration):
        answer = configuration.get_database().get_next_occurances(self.food)
        message = ""
        if not answer:
            message = "Sorry, we couldn't find anything like " + self.food + " in our database :("
        else:
            meal = answer[0][0]
            food_item = answer[0][1]
            self.food = food_item.name
            self.location = meal.d_hall
            self.time = meal.name
            message = "Next: " + self.food + ", " + self.location + ", " + self.time + ", " + meal.date.strftime('%m/%d/%Y')

        configuration.send_message(message)
        return message



class CurrentStatusQuery(Query):

    def __init__(self, food, location=""):
        self.food = food
        self.location = location

    def apply(self, configuration):
        answer = configuration.get_database().get_current_status()
        message = ""
        if not answer:
            message = "Sorry, we couldn't find anything :("
        else:
            meal = answer[0][0]
            food_item = answer[0][1]
            self.location = meal.d_hall
            self.time = meal.name
            message = "Now: " + self.food + ", " + self.location

        configuration.send_message(message)
        return message
        #configuration.send_message("Now: " + self.food + ", " + self.location)

