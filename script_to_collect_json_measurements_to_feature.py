import json
import re

import numpy as np
import pandas as pd

from algorithms import TSP
from algorithms.ant_colony_scikitopt.AntColonyTspScikitopt import AntColonyTspScikitopt
from algorithms.astar.Astar import Astar
from algorithms.brutalforce.BruteForce import BrutalForceTsp
from algorithms.dynamic_programing_held_karp.DynamicProgramingTsp import DynamicProgramingHeldKarpTsp
from algorithms.genetic_algorithm_mlrose.GeneticAlgorithmMlroseTsp import GeneticAlgorithmMlroseTsp
from algorithms.greedy_search.GreadySearchTsp import GreedySearchTsp
from algorithms.local_search.LocalSearchTsp import LocalSearchTsp
from algorithms.simulated_annealing.SimulatedAnnealing import SimulatedAnnealingTsp
from builders.PathBuilder import PathBuilder
from constants import MeasurementBasic
from constants.AlgNames import *
from constants.AlgNamesResults.names import *
from constants.FileExtensions import JSON, CSV
from constants.MeasurementBasic import *
from constants.MeasurementCpuProfiler import *
from constants.MeasurementMemory import *
from constants.MeasurementTimeWithOutputData import *
from constants.MeasurementsTypes import *
from data_reader import JsonTspReader
from functions import exist_file
from input.TspInputData import TspInputData

DISTANCE = 1000
NAME_OF_MEASUREMENT_DIR = "measurements"
NAME_OF_DATASET_DIR = "dataset"
NAME_FILE = "raw_tsp_results"
JSON_DATA = "JSON_DATA"
PATH_TO_JSON = "PATH_TO_JSON"
TSP_INPUT_OBJECT = "TSP_INPUT_OBJECT"
PATTERN_TO_OUTPUT_DIRECTORY_FROM_NAME_OF_SAMPLE = "TSP_MEASUREMENTS_FROM_SET_%d_N_%d"
PATTERN_TO_DIRECTORY_FROM_DATASET = "TSP_DIST_%d_N_%d"
PATTERN_TO_FILE_NAME_OF_SAMPLE = "TSP_CITIES_SET_%d_N_%d.json"


def prepare_algorithm(name_of_algorithm, data_to_inject):
    switcher = {
        ASTAR: Astar(data_to_inject),
        BRUTAL_FORCE: BrutalForceTsp(data_to_inject),
        DYNAMIC_PROGRAMING_HELD_KARP: DynamicProgramingHeldKarpTsp(data_to_inject),
        GENETIC_ALGORITHM_MLROSE: GeneticAlgorithmMlroseTsp(data_to_inject),
        GREEDY_SEARCH: GreedySearchTsp(data_to_inject),
        LOCAL_SEARCH: LocalSearchTsp(data_to_inject),
        SIMULATED_ANNEALING: SimulatedAnnealingTsp(data_to_inject),
        ANT_COLONY_TSP: AntColonyTspScikitopt(data_to_inject)
    }
    return switcher.get(name_of_algorithm, "Invalid name of algorithm")


def prepare_path_to_src_tsp_json(name_of_dir_with_samples, name_of_file_name_sample):
    return PathBuilder() \
        .add_dir(NAME_OF_DATASET_DIR) \
        .add_dir(name_of_dir_with_samples) \
        .add_file_with_extension(name_of_file_name_sample) \
        .build()


def prepare_path_to_json_result(name_of_dir_for_measurements, name_of_alg_dir_results, number_of_city, measurement):
    return PathBuilder() \
        .add_dir(NAME_OF_MEASUREMENT_DIR) \
        .create_directory_if_not_exists() \
        .add_dir(JSON) \
        .create_directory_if_not_exists() \
        .add_dir("N_%d" % number_of_city) \
        .create_directory_if_not_exists() \
        .add_dir(name_of_dir_for_measurements) \
        .create_directory_if_not_exists() \
        .add_dir(name_of_alg_dir_results) \
        .create_directory_if_not_exists() \
        .add_file(measurement, JSON) \
        .build()


def get_name_dir_on_results(name_of_algorithm):
    switcher = {
        ASTAR: ASTAR_HEURISTIC_SELF_IMPL_DIR,
        BRUTAL_FORCE: BRUTAL_FORCE_LIB_PYTHON_TSP_DIR,
        DYNAMIC_PROGRAMING_HELD_KARP: DYNAMIC_PROGRAMING_EXAC_HELD_KARP_LIB_DIR,
        GENETIC_ALGORITHM_MLROSE: GENETIC_ALGORITHM_HEURISTIC_LIB_MLROSE_DIR,
        GENETIC_ALGORITHM_SCIKIT_OPT: GENETIC_ALGORITHM_HEURISTIC_LIB_SCIKIT_OPT_DIR,
        PARTICLE_SWARM_TSP: PARTICLE_SWARM_OPT_TSP_DIR,
        GREEDY_SEARCH: GREEDY_SEARCH_HEURISTIC_SELF_IMPL_DIR,
        LOCAL_SEARCH: LOCAL_SEARCH_HEURISTIC_LIB_PYTHON_TSP_DIR,
        SIMULATED_ANNEALING: SIMULATED_ANNEALING_HEURISTIC_LIB_PYTHON_TSP_DIR,
        ANT_COLONY_TSP: ANT_COLONY_TSP_SCIKIT_OPT_DIR
    }
    return switcher.get(name_of_algorithm, "Invalid name of algorithm")


def is_valid_way_as_str(actual_path_as_str, number_of_cities):
    actual_path_as_list = json.loads(actual_path_as_str)
    first_node = actual_path_as_list[0]
    end_node = actual_path_as_list[len(actual_path_as_list) - 1]
    return first_node == end_node and len(actual_path_as_list) == number_of_cities + 1


def is_valid_way_as_array(actual_path_as_array, number_of_cities):
    actual_path_as_list = actual_path_as_array.tolist()
    first_node = actual_path_as_list[0]
    end_node = actual_path_as_list[len(actual_path_as_list) - 1]
    return first_node == end_node and len(actual_path_as_list) == number_of_cities + 1


def is_valid_way_as_list(actual_path_as_list, number_of_cities):
    first_node = actual_path_as_list[0]
    end_node = actual_path_as_list[len(actual_path_as_list) - 1]
    return first_node == end_node and len(actual_path_as_list) == number_of_cities + 1


def is_valid_way_for_any_type(way_to_valid, number_of_cities):
    if type(way_to_valid) == list:
        return is_valid_way_as_list(way_to_valid, number_of_cities)
    if type(way_to_valid) == str:
        return is_valid_way_as_str(way_to_valid, number_of_cities)
    if type(way_to_valid) == np.ndarray:
        return is_valid_way_as_array(way_to_valid, number_of_cities)
    else:
        raise Exception("Not recognize type of way")


def convert_way_in_any_type_to_int_list(way_in_any_type):
    if type(way_in_any_type) == list:
        integer_map = map(int, way_in_any_type)
        return list(integer_map)
    if type(way_in_any_type) == str:
        list_str = json.loads(way_in_any_type)
        integer_map = map(int, list_str)
        return list(integer_map)
    if type(way_in_any_type) == np.ndarray:
        return way_in_any_type.tolist()
    else:
        raise Exception("Not recognize type of way")


def check_if_list_has_duplicated_elements(list_of_elements):
    if len(list_of_elements) == len(set(list_of_elements)):
        return False
    else:
        return True


def customize_way(way_as_list_of_int, number_of_cities, expected_start_end_node):
    if check_if_list_has_duplicated_elements(way_as_list_of_int):
        return TSP.shuffle_solution_set_start_and_end_node_as_the_same(way_as_list_of_int, expected_start_end_node)
    else:
        processed_way = way_as_list_of_int
        if way_as_list_of_int[0] != expected_start_end_node:
            tmp_list = [expected_start_end_node]
            for node in way_as_list_of_int:
                tmp_list.append(node)
            processed_way = tmp_list
        if way_as_list_of_int[len(way_as_list_of_int) - 1] != 0:
            tmp_list = processed_way
            tmp_list.append(expected_start_end_node)
            processed_way = tmp_list
        if len(processed_way) != number_of_cities + 1:
            raise Exception("Path contain %d elements NOT expected %d elements path: %s" % (
                len(processed_way), number_of_cities + 1, processed_way))
    return processed_way


def merge_dictionarys(list_dictionarys):
    result_dict = dict()
    for dictionary in list_dictionarys:
        for key in dictionary.keys():
            if key not in result_dict:
                result_dict[key] = dictionary[key]
    return result_dict


def prepare_dict_alg_per_n_cities_per_index_sample_per_measure_type_and_faulty_path_json_list(name_of_algorithm_list,
                                                                                              number_of_city_list,
                                                                                              index_of_sample_list,
                                                                                              type_measurement_list):
    inner_dict_alg_per_n_cities_per_index_sample_per_measure_type = dict()
    faulty_files = list()
    for alg in name_of_algorithm_list:
        inner_dict_alg_per_n_cities_per_index_sample_per_measure_type[alg] = dict()
        for n_cites in number_of_city_list:
            inner_dict_alg_per_n_cities_per_index_sample_per_measure_type[alg][n_cites] = dict()
            for index_of_sample in index_of_sample_list:
                inner_dict_alg_per_n_cities_per_index_sample_per_measure_type[alg][n_cites][index_of_sample] = dict()
                for type_of_measure in type_measurement_list:
                    inner_dict_alg_per_n_cities_per_index_sample_per_measure_type[alg][n_cites][index_of_sample][
                        type_of_measure] = dict()
                    name_of_alg_dir_results = get_name_dir_on_results(alg)
                    name_of_dir_for_measurements = PATTERN_TO_OUTPUT_DIRECTORY_FROM_NAME_OF_SAMPLE % (
                        index_of_sample, n_cites)
                    path_to_json_result = prepare_path_to_json_result(name_of_dir_for_measurements,
                                                                      name_of_alg_dir_results,
                                                                      n_cites, type_of_measure)
                    if exist_file(path_to_json_result):
                        json_data = JsonTspReader.read_json_from_path(path_to_json_result)
                        name_of_dir_with_samples = PATTERN_TO_DIRECTORY_FROM_DATASET % (DISTANCE, n_cites)
                        name_of_file_name_sample = PATTERN_TO_FILE_NAME_OF_SAMPLE % (index_of_sample, n_cites)
                        path_to_src_tsp_json = prepare_path_to_src_tsp_json(name_of_dir_with_samples,
                                                                            name_of_file_name_sample)
                        json_src_data = JsonTspReader.read_json_from_path(path_to_src_tsp_json)
                        inner_dict_alg_per_n_cities_per_index_sample_per_measure_type[alg][n_cites][index_of_sample][
                            type_of_measure][PATH_TO_JSON] = path_to_json_result
                        inner_dict_alg_per_n_cities_per_index_sample_per_measure_type[alg][n_cites][index_of_sample][
                            type_of_measure][JSON_DATA] = json_data
                        inner_dict_alg_per_n_cities_per_index_sample_per_measure_type[alg][n_cites][index_of_sample][
                            type_of_measure][TSP_INPUT_OBJECT] = TspInputData(json_src_data)
                    else:
                        faulty_files.append(path_to_json_result)
    return inner_dict_alg_per_n_cities_per_index_sample_per_measure_type, faulty_files


def init_dictionary_by_keys_from_list_and_empty_list_as_values(list_of_keys):
    result_dictionary = dict()
    for name_as_key in list_of_keys:
        result_dictionary[name_as_key] = list()
    return result_dictionary


def get_number_of_city_from_src_name(src_tsp_file):
    numbers = [int(s) for s in re.findall(r'\d+', src_tsp_file)]
    return numbers[1]


def get_index_of_sample_from_src_name(src_tsp_file):
    numbers = [int(s) for s in re.findall(r'\d+', src_tsp_file)]
    return numbers[0]


NUMBER_OF_CITIES = list(range(4, 16))
INDEXES_OF_SAMPLES = list(range(0, 100))
NAMES_OF_ALGORITHMS = [ASTAR,
                       GREEDY_SEARCH,
                       LOCAL_SEARCH,
                       SIMULATED_ANNEALING,
                       BRUTAL_FORCE,
                       DYNAMIC_PROGRAMING_HELD_KARP,
                       GENETIC_ALGORITHM_MLROSE,
                       GENETIC_ALGORITHM_SCIKIT_OPT,
                       PARTICLE_SWARM_TSP,
                       ANT_COLONY_TSP
                       ]
TYPE_OF_MEASUREMENT = [CPU, TIME_AND_DATA, TIME_AND_MEMORY]
total = len(NUMBER_OF_CITIES) * len(INDEXES_OF_SAMPLES) * len(NAMES_OF_ALGORITHMS) * len(TYPE_OF_MEASUREMENT)
current = 0
column_names = [
    USED_ALGORITHM,  # ALL
    NAME_OF_SRC_FILE,  # ALL
    MeasurementBasic.NUMBER_OF_CITIES,  # FROM NAME_OF_SRC_FILE
    MeasurementBasic.NUMBER_OF_SAMPLE,  # FROM NAME_OF_SRC_FILE
    BEST_WAY,  # TIME_AND_DATA
    FULL_COST,
    HAMILTONIAN_CYCLE_COST,  # FROM BEST_WAY
    TIME_DURATION_WITHOUT_MALLOC_IN_SEC,  # TIME_AND_DATA
    UTILIZATION_OF_CPU,  # CPU
    USED_MEMORY_AFTER_MEASUREMENT_IN_BYTES,  # TIME_AND_MEMORY
    USED_MEMORY_PEAK_AFTER_MEASUREMENT_IN_BYTES  # TIME_AND_MEMORY
]
RESULT_DICT = init_dictionary_by_keys_from_list_and_empty_list_as_values(column_names)
dict_alg_per_n_cities_per_index_sample_per_measure_type, faulty_json_paths = \
    prepare_dict_alg_per_n_cities_per_index_sample_per_measure_type_and_faulty_path_json_list(NAMES_OF_ALGORITHMS,
                                                                                              NUMBER_OF_CITIES,
                                                                                              INDEXES_OF_SAMPLES,
                                                                                              TYPE_OF_MEASUREMENT)
dict_json = dict_alg_per_n_cities_per_index_sample_per_measure_type
files_with_wrong_paths = list()
for alg_name in dict_json.keys():
    for number_of_cities in dict_json[alg_name].keys():
        for index_of_sample in dict_json[alg_name][number_of_cities].keys():
            for type_of_measure in dict_json[alg_name][number_of_cities][index_of_sample].keys():
                if JSON_DATA in dict_json[alg_name][number_of_cities][index_of_sample][type_of_measure]:
                    json_data = dict_json[alg_name][number_of_cities][index_of_sample][type_of_measure][JSON_DATA]
                    tsp_input_object = dict_json[alg_name][number_of_cities][index_of_sample][type_of_measure][
                        TSP_INPUT_OBJECT]
                    path_to_result_path = dict_json[alg_name][number_of_cities][index_of_sample][type_of_measure][
                        PATH_TO_JSON]
                    if type_of_measure == CPU:
                        src_name_of_file = json_data[NAME_OF_SRC_FILE]
                        used_algorithm = json_data[USED_ALGORITHM]
                        RESULT_DICT[USED_ALGORITHM].append(used_algorithm)
                        RESULT_DICT[NAME_OF_SRC_FILE].append(src_name_of_file)
                        RESULT_DICT[MeasurementBasic.NUMBER_OF_CITIES].append(number_of_cities)
                        RESULT_DICT[MeasurementBasic.NUMBER_OF_SAMPLE].append(index_of_sample)
                        RESULT_DICT[UTILIZATION_OF_CPU].append(json_data[UTILIZATION_OF_CPU])
                    if type_of_measure == TIME_AND_DATA:
                        best_way = json_data[BEST_WAY]
                        src_name_of_file = json_data[NAME_OF_SRC_FILE]
                        number_cities = get_number_of_city_from_src_name(src_name_of_file)
                        if not is_valid_way_for_any_type(best_way, number_cities):
                            files_with_wrong_paths.append(path_to_result_path)
                        hamiltonian_cycle_cost = tsp_input_object.cal_total_distance(best_way)
                        RESULT_DICT[BEST_WAY].append(best_way)
                        RESULT_DICT[FULL_COST].append(json_data[FULL_COST])
                        RESULT_DICT[TIME_DURATION_WITHOUT_MALLOC_IN_SEC].append(
                            json_data[TIME_DURATION_WITHOUT_MALLOC_IN_SEC])
                        RESULT_DICT[HAMILTONIAN_CYCLE_COST].append(hamiltonian_cycle_cost)
                    if type_of_measure == TIME_AND_MEMORY:
                        RESULT_DICT[USED_MEMORY_AFTER_MEASUREMENT_IN_BYTES].append(
                            json_data[USED_MEMORY_AFTER_MEASUREMENT_IN_BYTES])
                        RESULT_DICT[USED_MEMORY_PEAK_AFTER_MEASUREMENT_IN_BYTES].append(
                            json_data[USED_MEMORY_PEAK_AFTER_MEASUREMENT_IN_BYTES])
result_df = pd.DataFrame(RESULT_DICT)
result_df.replace("", np.nan, inplace=True)
result_df = result_df.dropna()
# print(results_measurements_dict)
feature_result_path = PathBuilder() \
    .add_dir("results_tsp") \
    .create_directory_if_not_exists() \
    .add_file(NAME_FILE, CSV) \
    .build()
# result_df.to_csv(feature_result_path)
# print("Created new csv file :\n %s" % feature_result_path)
print("NOT_EXISTS_JSONS")
print(faulty_json_paths)
# print("JSON_RESULTS_WITH_FAULTY WAYS")
# print(files_with_wrong_paths)
