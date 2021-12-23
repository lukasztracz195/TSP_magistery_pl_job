import json
from argparse import ArgumentParser

from algorithms.astar.Astar import Astar
from algorithms.brutalforce.BruteForce import BrutalForceTsp
from algorithms.dynamic_programing_held_karp.DynamicProgramingTsp import DynamicProgramingHeldKarpTsp
from algorithms.genetic_algorithm_mlrose.GeneticAlgorithmMlroseTsp import GeneticAlgorithmMlroseTsp
from algorithms.greedy_search.GreadySearchTsp import GreedySearchTsp
from algorithms.local_search.LocalSearchTsp import LocalSearchTsp
from algorithms.simulated_annealing.SimulatedAnnealing import SimulatedAnnealingTsp
from builders.PathBuilder import PathBuilder
from collector.DataCollector import DataCollector
from constants.AlgNames import *
from constants.ArgNames import *
from constants.FileExtensions import JSON
from constants.MeasurementBasic import *
from data_reader import JsonTspReader
from input.TspInputData import TspInputData

# ALGORITHMS
# Astar 3-60 DONE
# BrutalForceTsp 3-10
# DynamicProgramingHeldKarpTsp 3-60
# GeneticAlgorithmMlroseTsp 3-60
# GreedySearchTsp 3-60
# LocalSearchTsp 3-60
# SimulatedAnnealingTsp 3-60
AVAILABLE_ALGORITHM_NAMES = ["Astar", "BrutalForceTsp", "DynamicProgramingHeldKarpTsp", "GeneticAlgorithmMlroseTsp",
                             "GreedySearchTsp", "LocalSearchTsp", "SimulatedAnnealingTsp"]
PATTERN_TO_DIRECTORY_FROM_DATASET = "TSP_DIST_%d_N_%d"
PATTERN_TO_FILE_NAME_OF_SAMPLE = "TSP_CITIES_SET_%d_N_%d.json"
PATTERN_TO_OUTPUT_DIRECTORY_FROM_NAME_OF_SAMPLE = "TSP_MEASUREMENTS_FROM_SET_%d_N_%d"
NAME_OF_DATASET_DIR = "dataset"
NAME_OF_MEASUREMENT_DIR = "measurements"
parser = ArgumentParser()
parser.add_argument(NAME_OF_ALGORITHM, help="name of algorithm to solve TSP problem\n%s" \
                                            % AVAILABLE_ALGORITHM_NAMES, type=str)
parser.add_argument(NUMBER_OF_CITIES, help="number of cities to select correct dir with samples from dataset",
                    type=int)
parser.add_argument(NUMBER_OF_SAMPLE, help="number of sample witch contain input TSP data", type=int)
parser.add_argument(TYPE_OF_MEASUREMENT, help="type of measurement: CPU, TIME_AND_DATA, TIME_AND_MEMORY", type=str)
args = parser.parse_args()

DISTANCE = 1000
NAME_OF_ALGORITHM = args.name_of_algorithm
NUMBER_OF_CITIES = args.number_of_cities
NUMBER_OF_SAMPLE = args.number_of_sample
MEASUREMENT = args.type_of_measurement


def prepare_algorithm(name_of_algorithm, data_to_inject):
    switcher = {
        ASTAR: Astar(data_to_inject),
        BRUTAL_FORCE: BrutalForceTsp(data_to_inject),
        DYNAMIC_PROGRAMING_HELD_KARP: DynamicProgramingHeldKarpTsp(data_to_inject),
        GENETIC_ALGORITHM: GeneticAlgorithmMlroseTsp(data_to_inject),
        GREEDY_SEARCH: GreedySearchTsp(data_to_inject),
        LOCAL_SEARCH: LocalSearchTsp(data_to_inject),
        SIMULATED_ANNEALING: SimulatedAnnealingTsp(data_to_inject)
    }
    return switcher.get(name_of_algorithm, "Invalid name of algorithm")


def make_measurement(algorithm) -> DataCollector:
    if MEASUREMENT == "CPU":
        return algorithm.start_counting_with_cpu_profiler()
    if MEASUREMENT == "TIME_AND_DATA":
        return algorithm.start_counting_with_time()
    if MEASUREMENT == "TIME_AND_MEMORY":
        return algorithm.start_counting_with_time_and_trace_malloc()


def main():
    name_of_dir_with_samples = PATTERN_TO_DIRECTORY_FROM_DATASET % (DISTANCE, NUMBER_OF_CITIES)
    name_of_file_name_sample = PATTERN_TO_FILE_NAME_OF_SAMPLE % (NUMBER_OF_SAMPLE, NUMBER_OF_CITIES)
    path_to_sample = PathBuilder() \
        .add_dir(NAME_OF_DATASET_DIR) \
        .add_dir(name_of_dir_with_samples) \
        .add_file_with_extension(name_of_file_name_sample) \
        .build()
    json_data = JsonTspReader.read_json_from_path(path_to_sample)
    tsp_input_data = TspInputData(json_data)
    algorithm = prepare_algorithm(NAME_OF_ALGORITHM, tsp_input_data)
    algorithm.clear_data_before_measurement()
    collector = make_measurement(algorithm)
    collector.add_data(USED_ALGORITHM, algorithm.name)
    collector.add_data(NAME_OF_SRC_FILE, name_of_file_name_sample)
    name_of_dir_for_measurements = PATTERN_TO_OUTPUT_DIRECTORY_FROM_NAME_OF_SAMPLE % (
        NUMBER_OF_SAMPLE, NUMBER_OF_CITIES)
    path_to_output_json = PathBuilder() \
        .add_dir(NAME_OF_MEASUREMENT_DIR) \
        .add_dir(JSON) \
        .add_dir("N_%d" % NUMBER_OF_CITIES) \
        .create_directory_if_not_exists() \
        .add_dir(name_of_dir_for_measurements) \
        .create_directory_if_not_exists() \
        .add_dir(algorithm.name) \
        .create_directory_if_not_exists() \
        .add_file(MEASUREMENT, JSON) \
        .build()
    json_result_data = json.dumps(collector.get_dictionary_with_data())
    with open(path_to_output_json, 'w') as outfile:
        outfile.write(json_result_data)


if __name__ == "__main__":
    main()
