import json

import numpy as np

from input.TspCityJsonData import TspCityJsonData
from input.TspLibData import TspLibData

PATH_TO_TSP_DATA_LIB = ""


class TspInputData:

    def __init__(self, tsp_data_json):
        self.tsp_city_json_data = TspCityJsonData(tsp_data_json)
        self.is_tsplib = False

        self.selected_city_on_start = 0
        self.list_of_cities = self.tsp_city_json_data.list_of_cities
        self.cost_matrix = self.tsp_city_json_data.cost_matrix
        self.number_of_cities = self.tsp_city_json_data.number_of_cities
        self.graph = self.tsp_city_json_data.graph
        self.dist_list = self.tsp_city_json_data.dist_list
        self.coord_list = self.tsp_city_json_data.coord_list

    # def __init__(self, path_to_src_tsp_lib, is_tsplib):
    #     self.tsp_lib_data = TspLibData(path_to_src_tsp_lib)
    #     self.is_tsplib = is_tsplib
    #
    #     self.selected_city_on_start = 0
    #     self.list_of_cities = self.tsp_lib_data.list_of_cities
    #     self.cost_matrix = self.tsp_lib_data.cost_matrix
    #     self.number_of_cities = self.tsp_lib_data.number_of_cities
    #     self.graph = self.tsp_lib_data.graph
    #     self.dist_list = self.tsp_lib_data.dist_list
    #     self.coord_list = self.tsp_lib_data.coord_list

    def cal_total_distance(self, routine):
        way_as_list = list()
        if type(routine) == list:
            way_as_list = routine
        if type(routine) == np.ndarray:
            way_as_list = routine.tolist()
        sum_value = 0.0
        number_of_cities = len(way_as_list)
        src_index = 0
        dest_index = 1
        while dest_index < number_of_cities - 1:
            dest_index = src_index + 1
            src_city = way_as_list[src_index]
            dest_city = way_as_list[dest_index]
            distance = self.get_distance(src_city, dest_city)
            sum_value += distance
            src_index += 1
        return sum_value

    def get_distance(self, index_of_city_1, index_of_city_2):
        return self.cost_matrix[index_of_city_1][index_of_city_2]

    def is_valid_way_as_str(self, actual_path_as_str):
        actual_path_as_list = json.loads(actual_path_as_str)
        first_node = actual_path_as_list[0]
        end_node = actual_path_as_list[len(actual_path_as_list) - 1]
        return first_node == end_node and len(actual_path_as_list) == self.number_of_cities + 1

    def is_valid_way_as_array(self, actual_path_as_array):
        actual_path_as_list = actual_path_as_array.tolist()
        first_node = actual_path_as_list[0]
        end_node = actual_path_as_list[len(actual_path_as_list) - 1]
        return first_node == end_node and len(actual_path_as_list) == self.number_of_cities + 1

    def is_valid_way_as_list(self, actual_path_as_list):
        first_node = actual_path_as_list[0]
        end_node = actual_path_as_list[len(actual_path_as_list) - 1]
        return first_node == end_node and len(actual_path_as_list) == self.number_of_cities + 1

    def is_valid_way_for_any_type(self, way_to_valid):
        if type(way_to_valid) == list:
            return self.is_valid_way_as_list(way_to_valid)
        if type(way_to_valid) == str:
            return self.is_valid_way_as_str(way_to_valid)
        if type(way_to_valid) == np.ndarray:
            return self.is_valid_way_as_array(way_to_valid)
        else:
            raise Exception("Not recognize type of way")
