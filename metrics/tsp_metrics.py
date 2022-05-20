import pickle
import json

from builders.PathBuilder import PathBuilder
from constants.CsvColumnNames import *
from data_reader.JsonTspReader import read_solution_from_tsp_lib_file

PATH_TO_DICTIONARY_CONTAIN_OPTIMAL_RESULTS = PathBuilder() \
    .add_dir("optimal_tsp_results_as_dict") \
    .add_file_with_extension("optimal_tsp_results_dict.pkl") \
    .build()


# { name_of_src_tsp_file: {
#     BEST_WAY: [0,1,2,3,0],
# HAMILTONIAN_CYCLE_COST: 45.45
# }
class TspOptimalVerifier:

    def __init__(self, src_tsp_file_name, tsp_path_to_verify, tsp_cost_to_verify,tsp_input_data_object, is_tsp_lib=False):
        self.__tsp_path_to_verify = tsp_path_to_verify
        self.__tsp_cost_to_verify = tsp_cost_to_verify
        self.__tsp_input_data_object = tsp_input_data_object
        if is_tsp_lib:
            self.__optimal_way = read_solution_from_tsp_lib_file(src_tsp_file_name)
            self.__optimal_cost = self.__tsp_input_data_object.cal_total_distance(self.__optimal_way)
        else:
            a_file = open(PATH_TO_DICTIONARY_CONTAIN_OPTIMAL_RESULTS, "rb")
            self.__optimal_results_dir = pickle.load(a_file)
            self.__optimal_way = json.loads(self.__optimal_results_dir[src_tsp_file_name][BEST_WAY])
            self.__optimal_cost = self.__optimal_results_dir[src_tsp_file_name][HAMILTONIAN_CYCLE_COST]


    @property
    def optimal_way(self):
        return self.__optimal_way

    @property
    def optimal_cost(self):
        return self.__optimal_cost

    @property
    def is_optimal_way(self):
        reversed_optimal = self.__optimal_way.copy()
        reversed_optimal.reverse()
        return self.__tsp_path_to_verify == self.__optimal_way or self.__tsp_path_to_verify == reversed_optimal

    @property
    def absolute_distance_error(self):
        if self.is_optimal_way:
            return 0.0
        error = self.__tsp_cost_to_verify - self.__optimal_cost
        if error < 1e-12:
            return 0.0
        return self.__tsp_cost_to_verify - self.__optimal_cost

    @property
    def relative_distance_error(self):
        if self.is_optimal_way:
            return 0.0
        fraction = (self.absolute_distance_error / self.__optimal_cost)
        return (fraction * 100)
