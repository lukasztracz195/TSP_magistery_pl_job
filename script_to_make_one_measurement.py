import json
import os
import sys

from algorithms.astar.Astar import Astar
from algorithms.brutalforce.BruteForce import BrutalForceTsp
from algorithms.genetic_algorithm_mlrose.GeneticAlgorithmMlroseTsp import GeneticAlgorithmMlroseTsp
from algorithms.greedy_search.GreadySearchTsp import GreedySearchTsp
from algorithms.simulated_annealing.SimulatedAnnealing import SimulatedAnnealingTsp
from data_reader.JsonTspReader import get_json_from_file

BEST_WAY = "best_way"
FULL_COST = "full_cost"
NAME_OF_SRC_FILE = "name_of_src_file"
TIME_DURATION_WITHOUT_MALLOC_IN_SEC = "time_duration_without_malloc_in_sec"
TIME_DURATION_WITH_MALLOC_IS_SEC = "time_duration_with_malloc_in_sec"
USED_MEMORY_IN_BYTES = "used_memory_in_bytes"
USED_PEAK_MEMORY_IN_BYTES = "used_peak_memory_in_bytes"
NUMBER_OF_SKIPPED_WAYS = "number_of_skipped_ways"
LOWER_BAND_ESTIMATED = "lower_band_estimated"
LOWER_BAND_ESTIMATED_USED_TO_COUNTING_WITHOUT_MALLOC = "lower_band_estimated_used_without_malloc"
LOWER_BAND_ESTIMATED_USED_TO_COUNTING_WITH_MALLOC = "lower_band_estimated_used_with_malloc"
USED_ALGORITHM = "used_algorithm"
N_SET = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 35, 40, 45, 50, 55, 60]

DATASET_DIR = "dataset"
RESULT_DATASET_DIR = "measurements/json/bruteforce"


def progress_bar(current, total, description='', barLength=20):
    percent = float(current) * 100 / total
    arrow = '-' * int(percent / 100 * barLength - 1) + '>'
    spaces = ' ' * (barLength - len(arrow))
    # if current % 10 == 0:
    sys.stdout.write('\rCounting progress: [%s%s] %f %% %s' % (arrow, spaces, percent, description))


NUMBER_OF_SET = 0
N = 4
current_path = os.getcwd()
NAME_OF_DIRECTORY = "TSP_DIST_1000_N_%d" % N
NAME_OF_JSON_FILE_WITH_EXTENSION = "TSP_CITIES_SET_0_N_%d.json" % N
global_path_to_dataset = "%s/%s/%s" % (current_path, DATASET_DIR, NAME_OF_DIRECTORY)
global_path_to_result_dataset = "%s/%s/%s" % (current_path, RESULT_DATASET_DIR, NAME_OF_DIRECTORY)
index_of_file = 0

json_data = get_json_from_file(NAME_OF_DIRECTORY, NAME_OF_JSON_FILE_WITH_EXTENSION)
alg = Astar(json_data)
json_model = alg.start_counting_with_time_and_trace_malloc()
print(json_model)
