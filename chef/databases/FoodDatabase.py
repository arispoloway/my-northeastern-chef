import abc


class FoodDatabase(abc.ABC):

    @abc.abstractmethod
    def get_next_occurances(self, food, dining_halls, max_occurances):
        raise NotImplementedError()



