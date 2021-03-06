import json

import numpy as np

from constants.InputCityDataJson import *
from models.City import City


class TspCityJsonData:

    def __init__(self, tsp_data_json):
        self.tsp_data_json = tsp_data_json
        self.selected_city_on_start = self.tsp_data_json[CITIES][0][NUMBER_OF_CITY]
        self.list_of_cities = None
        self.list_of_cities = self.__init_list_of_cities()
        self.cost_matrix = self.__prepare_cost_matrix()
        self.number_of_cities = len(self.tsp_data_json[CITIES])
        self.list_of_cities = self.__init_list_of_cities()
        self.graph = self.__prepare_graph()
        self.dist_list = self.__prepare_distance_list()
        self.coord_list = self.__prepare_coords_list()

    def __init_list_of_cities(self):
        if self.list_of_cities is not None and len(self.list_of_cities) > 0:
            return self.list_of_cities
        list_of_city = list()
        for city_dict in self.tsp_data_json[CITIES]:
            city = City(number_of_city=city_dict[NUMBER_OF_CITY], x=city_dict[X], y=city_dict[Y])
            list_of_city.append(city)
        return list_of_city

    def __prepare_cost_matrix(self):
        list_of_cities = self.__init_list_of_cities()
        number_of_cities = len(self.tsp_data_json[CITIES])
        matrix = np.zeros((number_of_cities, number_of_cities))
        for city_1 in list_of_cities:
            for city_2 in list_of_cities:
                distance = City.count_distance(city_1, city_2)
                matrix[city_1.number_of_city][city_2.number_of_city] = distance
        return matrix

    def get_distance(self, index_of_city_1, index_of_city_2):
        return self.cost_matrix[index_of_city_1][index_of_city_2]

    def __prepare_graph(self):
        list_of_cities = self.__init_list_of_cities()
        graph = dict()
        for city in list_of_cities:
            graph[city.number_of_city] = dict()
        for city_1 in list_of_cities:
            for city_2 in list_of_cities:
                distance = City.count_distance(city_1, city_2)
                if distance > 0:
                    graph[city_1.number_of_city][city_2.number_of_city] = distance
        return graph

    def __prepare_distance_list(self):
        list_of_cities = self.__init_list_of_cities()
        dist_list = []
        for city_1 in list_of_cities:
            for city_2 in list_of_cities:
                distance = City.count_distance(city_1, city_2)
                if distance > 0 and city_1.number_of_city < city_2.number_of_city:
                    tuple_item = (city_1.number_of_city, city_2.number_of_city, distance)
                    dist_list.append(tuple_item)
        return dist_list

    def __prepare_coords_list(self):
        list_of_cities = self.__init_list_of_cities()
        coord_list = []
        for city in list_of_cities:
            tuple_item = (city.x, city.y)
            coord_list.append(tuple_item)
        return coord_list
