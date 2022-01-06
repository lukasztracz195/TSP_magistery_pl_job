import numpy as np
import pandas as pd

from algorithms.ant_colony_scikitopt.AntColonyTspScikitopt import AntColonyTspScikitopt
from algorithms.astar.Astar import Astar
from algorithms.brutalforce.BruteForce import BrutalForceTsp
from algorithms.dynamic_programing_held_karp.DynamicProgramingTsp import DynamicProgramingHeldKarpTsp
from algorithms.genetic_algorithm_mlrose.GeneticAlgorithmMlroseTsp import GeneticAlgorithmMlroseTsp
from algorithms.greedy_search.GreadySearchTsp import GreedySearchTsp
from algorithms.local_search.LocalSearchTsp import LocalSearchTsp
from algorithms.simulated_annealing.SimulatedAnnealing import SimulatedAnnealingTsp
from builders.PathBuilder import PathBuilder
from constants.AlgNames import *
from constants.AlgNamesResults.names import *
from constants.FileExtensions import JSON, FEATHER, CSV
from constants.MeasurementTimeWithOutputData import BEST_WAY
from constants.MeasurementsTypes import *
from data_reader import JsonTspReader
from functions import exist_file

DISTANCE = 1000
NAME_OF_MEASUREMENT_DIR = "measurements"
NAME_FEATURE_FILE = "results_tsp"


def prepare_algorithm(name_of_algorithm, data_to_inject):
    switcher = {
        ASTAR: Astar(data_to_inject),
        BRUTAL_FORCE: BrutalForceTsp(data_to_inject),
        DYNAMIC_PROGRAMING_HELD_KARP: DynamicProgramingHeldKarpTsp(data_to_inject),
        GENETIC_ALGORITHM: GeneticAlgorithmMlroseTsp(data_to_inject),
        GREEDY_SEARCH: GreedySearchTsp(data_to_inject),
        LOCAL_SEARCH: LocalSearchTsp(data_to_inject),
        SIMULATED_ANNEALING: SimulatedAnnealingTsp(data_to_inject),
        ANT_COLONY_TSP: AntColonyTspScikitopt(data_to_inject)
    }
    return switcher.get(name_of_algorithm, "Invalid name of algorithm")


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
        GENETIC_ALGORITHM: GENETIC_ALGORITHM_HEURISTIC_LIB_MLROSE_DIR,
        GREEDY_SEARCH: GREEDY_SEARCH_HEURISTIC_SELF_IMPL_DIR,
        LOCAL_SEARCH: LOCAL_SEARCH_HEURISTIC_LIB_PYTHON_TSP_DIR,
        SIMULATED_ANNEALING: SIMULATED_ANNEALING_HEURISTIC_LIB_PYTHON_TSP_DIR,
        ANT_COLONY_TSP: ANT_COLONY_TSP_SCIKIT_OPT_DIR
    }
    return switcher.get(name_of_algorithm, "Invalid name of algorithm")


def customize_way(input_way):
    processed_way = input_way
    if input_way[0] != 0:
        tmp_list = [0]
        for node in input_way:
            tmp_list.append(node)
        processed_way = tmp_list
    if input_way[len(input_way) - 1] != 0:
        tmp_list = processed_way
        tmp_list.append(0)
        processed_way = tmp_list
    return processed_way

def merge_dictionarys(list_dictionarys):
    result_dict = dict()
    for dictionary in list_dictionarys:
        for key in dictionary.keys():
            if key not in result_dict:
                result_dict[key] = dictionary[key]
    return result_dict


PATTERN_TO_OUTPUT_DIRECTORY_FROM_NAME_OF_SAMPLE = "TSP_MEASUREMENTS_FROM_SET_%d_N_%d"

NUMBER_OF_CITIES = list(range(3, 16))
INDEXES_OF_SAMPLES = list(range(0, 11))
NAMES_OF_ALGORITHMS = [ASTAR,
                       GREEDY_SEARCH,
                       LOCAL_SEARCH,
                       SIMULATED_ANNEALING,
                       BRUTAL_FORCE,
                       DYNAMIC_PROGRAMING_HELD_KARP,
                       GENETIC_ALGORITHM,
                       ANT_COLONY_TSP]
TYPE_OF_MEASUREMENT = [CPU, TIME_AND_DATA, TIME_AND_MEMORY]
total = len(NUMBER_OF_CITIES) * len(INDEXES_OF_SAMPLES) * len(NAMES_OF_ALGORITHMS) * len(TYPE_OF_MEASUREMENT)
current = 0
result_df = None
faulty_files = []
all_dictionarys = list()
columns = None
RESULT_DICT = dict()
for alg in NAMES_OF_ALGORITHMS:
    for n_cites in NUMBER_OF_CITIES:
        for index_of_sample in INDEXES_OF_SAMPLES:
            list_of_paths_to_results_of_json = list()
            for type_of_measure in TYPE_OF_MEASUREMENT:
                name_of_alg_dir_results = get_name_dir_on_results(alg)
                name_of_dir_for_measurements = PATTERN_TO_OUTPUT_DIRECTORY_FROM_NAME_OF_SAMPLE % (
                    index_of_sample, n_cites)
                path_to_json_result = prepare_path_to_json_result(name_of_dir_for_measurements, name_of_alg_dir_results,
                                                                  n_cites, type_of_measure)
                list_of_paths_to_results_of_json.append(path_to_json_result)
            list_dicts = list()
            for path_to_json in list_of_paths_to_results_of_json:
                if exist_file(path_to_json):
                    json_data = JsonTspReader.read_json_from_path(path_to_json)
                    list_dicts.append(json_data)
                else:
                    print("Not found json: ", path_to_json)
            if len(list_dicts) != 0:
                results_measurements_dict = merge_dictionarys(list_dicts)
                if columns is None:
                    columns = list(results_measurements_dict.keys())
                all_dictionarys.append(results_measurements_dict)
for column in columns:
    RESULT_DICT[column] = list()
for dictionary in all_dictionarys:
    for column in columns:
        if column in dictionary:
            if column == "used_algorithm" and dictionary[column] == ANT_COLONY_TSP_SCIKIT_OPT_DIR:
                print()
            if type(dictionary[column]) is list and len(dictionary[column]) == 1:
                dictionary[column] = dictionary[column][0]
        else:
            dictionary[column] = None
        RESULT_DICT[column].append(dictionary[column])
result_df = pd.DataFrame(RESULT_DICT)
result_df.replace("", np.nan, inplace=True)
result_df = result_df.dropna()
ways = result_df[BEST_WAY]
new_ways = list()
for way in ways:
    new_ways.append(customize_way(way))
new_ways = pd.Series(new_ways)
result_df[BEST_WAY] = new_ways
# print(results_measurements_dict)
feature_result_path = PathBuilder() \
    .add_dir("results_tsp") \
    .create_directory_if_not_exists() \
    .add_dir(FEATHER) \
    .create_directory_if_not_exists() \
    .add_file(NAME_FEATURE_FILE, CSV) \
    .build()
result_df.to_csv(feature_result_path)
print("FAULTY JSONS")
print(faulty_files)
