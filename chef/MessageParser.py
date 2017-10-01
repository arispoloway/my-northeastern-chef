from chef.Query import *


class MessageParser(object):

    @staticmethod
    def count_food_location_time_parse(split_message) -> (int, str, str, str):
        count = 0
        food = ""
        location = ""
        time = ""
        last_keyword = ""

        if split_message:
            try:
                count = int(split_message[0])
                split_message = split_message[1:]
            except:
                pass

        for word in split_message:
            if word == "at" or word == "for":
                last_keyword = word
            elif last_keyword == "at":
                location += word + " "
            elif last_keyword == "for":
                time += word + " "
            else:
                food += word + " "
        food = food.strip()
        location = location.strip()
        time = time.strip()

        return count, food, location, time

    @staticmethod
    def parse_message(message : str) -> Query:
        message = message.lower()
        if message.startswith("!next "):
            split_message = message.split()[1:]
            count, food, location, time = MessageParser.count_food_location_time_parse(split_message)

            if not food:
                return InvalidQuery("Invalid food")

            if count:
                return NextOccurrenceQuery(food, location, time, count)
            return NextOccurrenceQuery(food, location, time)

        if message.startswith("!now "):
            split_message = message.split()[1:]
            count, food, location, _ = MessageParser.count_food_location_time_parse(split_message)

            if not food:
                return InvalidQuery("Invalid food")

            return CurrentStatusQuery(food, location)
        if message.startswith("!test"):
            return TestQuery()
        
        if message.startswith("!help"):
            return HelpQuery()

        if message.startswith("!school"):
            split_message = message.split()[1:]
            if len(split_message) != 0:
                return SelectSchoolQuery(" ".join(split_message))
            else:
                return InvalidQuery("No school specified!")
        else:
            return InvalidQuery("")
        

