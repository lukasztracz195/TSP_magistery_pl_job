import random
from typing import List, Set

from models.City import City


class CityGenerator:
    def __init__(self, min_x, max_x, min_y, max_y, start_city):
        self.__min_x = min_x
        self.__max_x = max_x
        self.__min_y = min_y
        self.__max_y = max_y
        self.__start_city = start_city
        self.__forbidden_city = [self.__start_city]

    def generate_cities(self, number_of_cities, distinct=True):
        set_of_city = set()
        number_of_city = 1
        set_of_city.add(self.__start_city)
        while len(set_of_city) < number_of_cities:
            x = random.randint(self.__min_x, self.__max_x)
            y = random.randint(self.__min_y, self.__max_y)
            generated_city = City(number_of_city=number_of_city, x=x, y=y)
            if generated_city not in self.__forbidden_city:
                if distinct and generated_city not in set_of_city:
                    set_of_city.add(generated_city)
                    number_of_city += 1
        if type(set_of_city) == list:
            return set_of_city
        return list(set_of_city)
