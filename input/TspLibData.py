import json

import numpy as np

from data_reader.JsonTspReader import read_cities_from_tsp_lib_file
from models.City import City


class TspLibData:

    def __init__(self, path_to_src_tsp_lib):
        self.path_to_src_tsp_lib = path_to_src_tsp_lib

        self.selected_city_on_start = 0
        self.list_of_cities = read_cities_from_tsp_lib_file(path_to_src_tsp_lib)
        self.cost_matrix = self.__prepare_cost_matrix()
        self.number_of_cities = len(self.list_of_cities)
        self.graph = self.__prepare_graph()
        self.dist_list = self.__prepare_distance_list()
        self.coord_list = self.__prepare_coords_list()

    def __prepare_cost_matrix(self):
        list_of_cities = self.list_of_cities
        number_of_cities = len(list_of_cities)
        matrix = np.zeros((number_of_cities, number_of_cities))
        for city_1 in list_of_cities:
            for city_2 in list_of_cities:
                distance = City.count_distance(city_1, city_2)
                matrix[city_1.number_of_city][city_2.number_of_city] = distance
        return matrix

    def __prepare_graph(self):
        list_of_cities = self.list_of_cities
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
        list_of_cities = self.list_of_cities
        dist_list = []
        for city_1 in list_of_cities:
            for city_2 in list_of_cities:
                distance = City.count_distance(city_1, city_2)
                if distance > 0 and city_1.number_of_city < city_2.number_of_city:
                    tuple_item = (city_1.number_of_city, city_2.number_of_city, distance)
                    dist_list.append(tuple_item)
        return dist_list

    def __prepare_coords_list(self):
        list_of_cities = self.list_of_cities
        coord_list = []
        for city in list_of_cities:
            tuple_item = (city.x, city.y)
            coord_list.append(tuple_item)
        return coord_list