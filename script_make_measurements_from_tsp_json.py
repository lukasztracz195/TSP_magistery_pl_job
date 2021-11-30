import json
import os
import sys

from algorithms.astar.Astar import Astar
from algorithms.brutalforce.BruteForce import BrutalForceTsp
from algorithms.dynamic_programing_held_karp.DynamicProgramingTsp import DynamicProgramingHeldKarpTsp
from algorithms.genetic_algorithm_mlrose.GeneticAlgorithmMlroseTsp import GeneticAlgorithmMlroseTsp
from algorithms.greedy_search.GreadySearchTsp import GreedySearchTsp
from algorithms.local_search.LocalSearchTsp import LocalSearchTsp
from algorithms.simulated_annealing.SimulatedAnnealing import SimulatedAnnealingTsp
from data_reader.JsonTspReader import get_json_from_file
from models.tsp_json_measurement import MeasurementForTimeForGenetic, \
    MeasurementForTimeWithMallocForGenetic

NAME_OF_SRC_FILE = "name_of_src_file"
USED_ALGORITHM = "used_algorithm"

BEST_WAY = "best_way"
FULL_COST = "full_cost"

# measurement_duration
TIME_DURATION_WITHOUT_MALLOC_IN_SEC = "time_duration_without_malloc_in_sec"

# measurement_duration_and memory
TIME_DURATION_WITH_MALLOC_IS_SEC = "time_duration_with_malloc_in_sec"
MEMORY_ALLOCATED_IN_BYTES = "memory_allocated_in_bytes"
USED_MEMORY_BEFORE_MEASUREMENT_IN_BYTES = "used_memory_before_measurement_in_bytes"
USED_MEMORY_PEAK_BEFORE_MEASUREMENT_IN_BYTES = "used_memory_peak_before_measurement_in_bytes"
USED_MEMORY_DIFF_BEFORE_AFTER_MEASUREMENT_IN_BYTES = "used_memory_diff_before_after_measurement_in_bytes"
USED_MEMORY_DIFF_PEAK_BEFORE_AFTER_MEASUREMENT_IN_BYTES = "used_memory_peak_diff_before_after_measurement_in_bytes"
USED_MEMORY_AFTER_MEASUREMENT_IN_BYTES = "used_memory_after_measurement_in_bytes"
USED_MEMORY_PEAK_AFTER_MEASUREMENT_IN_BYTES = "used_memory_peak_after_measurement_in_bytes"

# genetic_algorithm
SIZE_OF_POPULATION = "size_of_population"
PROBABILITY_OF_MUTATION = "probability_of_mutation"
MAX_ATTEMPTS = "max_attempts"
MAX_ITERATIONS = "max_iterations"
RANDOM_STATE = "random_state"


def progress_bar(current, total, description='', barLength=20):
    percent = float(current) * 100 / total
    arrow = '-' * int(percent / 100 * barLength - 1) + '>'
    spaces = ' ' * (barLength - len(arrow))
    # if current % 10 == 0:
    sys.stdout.write('\rCounting progress: [%s%s] %f %% %s' % (arrow, spaces, percent, description))


def create_directory_if_not_exists(path):
    if not os.path.exists(path):
        os.mkdir(path)


def fill_json_frame_by_way_and_cost_solution(json_frame, json_model):
    json_frame[BEST_WAY] = json_model.best_trace
    json_frame[FULL_COST] = json_model.full_cost


def fill_json_frame_for_time_duration(json_frame, json_model):
    json_frame[TIME_DURATION_WITHOUT_MALLOC_IN_SEC] = json_model.time_duration_in_sec


def fill_json_fram_for_genetic_algorithm(json_frame, json_model):
    if isinstance(json_model, MeasurementForTimeForGenetic) or isinstance(json_model,
                                                                          MeasurementForTimeWithMallocForGenetic):
        json_frame[SIZE_OF_POPULATION] = json_model.size_of_population
        json_frame[PROBABILITY_OF_MUTATION] = json_model.probability_of_mutation
        json_frame[MAX_ATTEMPTS] = json_model.max_attempts
        json_frame[MAX_ITERATIONS] = json_model.max_iterations
        json_frame[RANDOM_STATE] = json_model.random_state


def fill_json_frame_for_time_duration_with_memory_measurement(json_frame, json_model):
    json_frame[TIME_DURATION_WITH_MALLOC_IS_SEC] = json_model.time_duration_in_sec
    json_frame[USED_MEMORY_BEFORE_MEASUREMENT_IN_BYTES] = json_model.used_memory_before_measurement
    json_frame[USED_MEMORY_PEAK_BEFORE_MEASUREMENT_IN_BYTES] = json_model.used_memory_peak_before_measurement
    json_frame[USED_MEMORY_DIFF_BEFORE_AFTER_MEASUREMENT_IN_BYTES] = json_model.used_memory_diff_before_after_measurement
    json_frame[USED_MEMORY_DIFF_PEAK_BEFORE_AFTER_MEASUREMENT_IN_BYTES] = json_model.used_memory_peak_diff_before_after_measurement
    json_frame[USED_MEMORY_AFTER_MEASUREMENT_IN_BYTES] = json_model.used_memory_after_measurement
    json_frame[USED_MEMORY_PEAK_AFTER_MEASUREMENT_IN_BYTES] = json_model.used_memory_peak_after_measurement

def fill_json_for_measure_of_timing(json_frame, json_model):
    fill_json_frame_by_way_and_cost_solution(json_frame, json_model)
    fill_json_frame_for_time_duration(json_frame, json_model)
    fill_json_fram_for_genetic_algorithm(json_frame, json_model)


def fill_json_for_measure_of_timieng_with_tracemalloc(json_frame, json_model):
    fill_json_frame_for_time_duration_with_memory_measurement(json_frame, json_model)
    fill_json_fram_for_genetic_algorithm(json_frame, json_model)


def prepare_name_of_directory_measurements_for_n_cities(number_of_all_samples, number_of_cities):
    return "TSP_DIST_%d_N_%d" % (number_of_all_samples, number_of_cities)


def prepare_name_of_measurement_file_sample(number_of_sample, number_of_cities, format_of_file):
    return "TSP_CITIES_SET_%d_N_%d.%s" % (number_of_sample, number_of_cities, format_of_file)


def prepare_global_path_to_two_wrapped_directory(name_of_directory_1, name_of_directory_2):
    current_path = os.getcwd()
    return "%s/%s/%s" % (current_path, name_of_directory_1, name_of_directory_2)


def prepare_global_path_to_wrapped_directory(name_of_directory_1):
    current_path = os.getcwd()
    return "%s/%s" % (current_path, name_of_directory_1)


def prepare_algorithm(name_of_algorithm, data_to_inject):
    switcher = {
        "Astar": Astar(data_to_inject),
        "BrutalForceTsp": BrutalForceTsp(data_to_inject),
        "DynamicProgramingHeldKarpTsp": DynamicProgramingHeldKarpTsp(data_to_inject),
        "GeneticAlgorithmMlroseTsp": GeneticAlgorithmMlroseTsp(data_to_inject),
        "GreedySearchTsp": GreedySearchTsp(data_to_inject),
        "LocalSearchTsp": LocalSearchTsp(data_to_inject),
        "SimulatedAnnealingTsp": SimulatedAnnealingTsp(data_to_inject)
    }
    return switcher.get(name_of_algorithm, "Invalid month")


def perform_measurement(algorithm):
    json_result = dict()
    global_path_to_result_dataset = prepare_global_path_to_two_wrapped_directory(RESULT_DATASET_DIR, algorithm.name)
    # global_path_to_result_dataset_file = prepare_global_path_to_two_wrapped_directory(
    #     name_of_directory_1="%s/%s" % (RESULT_DATASET_DIR, algorithm.name),
    #     name_of_directory_2=name_of_directory_with_data_for_n_cities)
    create_directory_if_not_exists(global_path_to_result_dataset)
    json_result[USED_ALGORITHM] = algorithm.name
    json_result[NAME_OF_SRC_FILE] = name_of_file

    json_model = algorithm.start_counting_with_time()
    fill_json_for_measure_of_timing(json_result, json_model)

    json_model = algorithm.start_counting_with_time_and_trace_malloc()
    fill_json_for_measure_of_timieng_with_tracemalloc(json_result, json_model)
    return json.dumps(json_result)


# N_SET = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 35, 40, 45, 50, 55, 60]
N_SET = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
# N_SET = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
# N_SET = [3, 4, 5, 6, 7, 8, 9, 10]

# ALGORITHMS
# Astar 3-60 DONE
# BrutalForceTsp 3-10
# DynamicProgramingHeldKarpTsp 3-60
# GeneticAlgorithmMlroseTsp 3-60
# GreedySearchTsp 3-60
# LocalSearchTsp 3-60
# SimulatedAnnealingTsp 3-60

DATASET_DIR = "dataset"
MEASUREMENTS_DIR = "measurements"
JSON = "json"
CSV = "csv"
RESULT_DATASET_DIR = "%s/%s" % (MEASUREMENTS_DIR, JSON)
NUMBER_OF_ALL_SAMPLES = 1000
number_of_sample = 0
NAME_OF_ALGORITHM = "SimulatedAnnealingTsp"
for number_of_cities_in_measurement in N_SET:
    name_of_directory_with_data_for_n_cities = \
        prepare_name_of_directory_measurements_for_n_cities(number_of_all_samples=
                                                            NUMBER_OF_ALL_SAMPLES,
                                                            number_of_cities=number_of_cities_in_measurement)
    name_of_file_with_data_to_start_measurement = prepare_name_of_measurement_file_sample(
        number_of_sample=number_of_sample,
        number_of_cities=number_of_cities_in_measurement,
        format_of_file=JSON)

    global_path_to_dataset = prepare_global_path_to_two_wrapped_directory(name_of_directory_1=DATASET_DIR,
                                                                          name_of_directory_2=name_of_directory_with_data_for_n_cities)
    index_of_file = 0
    for _, _, files in os.walk(global_path_to_dataset):
        total = len(files)
        for name_of_file in files:
            if name_of_file.endswith(JSON):
                data_fetched_to_perform_measurements = get_json_from_file(name_of_directory_with_data_for_n_cities,
                                                                          name_of_file)
                alg = prepare_algorithm(name_of_algorithm=NAME_OF_ALGORITHM,
                                        data_to_inject=data_fetched_to_perform_measurements)
                global_path_to_result_dataset_file = prepare_global_path_to_two_wrapped_directory(
                    name_of_directory_1="%s/%s" % (RESULT_DATASET_DIR, alg.name),
                    name_of_directory_2=name_of_directory_with_data_for_n_cities)

                json_as_str = perform_measurement(alg)

                create_directory_if_not_exists(global_path_to_result_dataset_file)
                path_to_json_file = global_path_to_result_dataset_file + "/" + name_of_file
                jsons_file = open(path_to_json_file, "w")
                jsons_file.write(json_as_str)
                jsons_file.close()
                index_of_file += 1
                message = "number of cities: %s | name_of_used_algorithm: %s | last created file: %s" \
                          % (number_of_cities_in_measurement, alg.name, name_of_file)
                progress_bar(index_of_file, total, message)
        number_of_sample += 1
