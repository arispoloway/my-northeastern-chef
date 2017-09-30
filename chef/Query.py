import abc

from chef.Scheduler import Scheduler
from chef.database import FoodDatabaseSelector
from chef.database.FoodDatabase import FoodDatabase


def school_required(func):
    def wrapper(self, configuration):
        if not configuration.get_database():
            configuration.send_message("No school selected. Use !school <name> to select a school!")
            return
        func(self, configuration)
    return wrapper

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

    @school_required
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

    @school_required
    def apply(self, configuration):
        answer = configuration.get_database().get_current_status()
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


class SelectSchoolQuery(Query):
    def __init__(self, school):
        self.school = school

    def apply(self, configuration):
        if not FoodDatabaseSelector.get_school_database(self.school):
            configuration.send_message("Invalid school!")
        else:
            configuration.settings.set("school", self.school)
            configuration.send_message("School changed to '" + self.school + "'")


class TestQuery(Query):

    def apply(self, configuration):
        configuration.send_message("Testing!")
        
class HelpQuery(Query):
    def apply(self, configuration):
        configuration.send_message("Current Commands: \n !test : Tests is the bot is responding. \n !register : Register yourself to the bot. \n !next <food> : When is <food> showing up next? \n !school <school> : Change school.")

