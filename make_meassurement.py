from argparse import ArgumentParser
import logging
from algorithms.astar.Astar import Astar
from algorithms.brutalforce.BruteForce import BrutalForceTsp
from algorithms.dynamic_programing_held_karp.DynamicProgramingTsp import DynamicProgramingHeldKarpTsp
from algorithms.genetic_algorithm_mlrose.GeneticAlgorithmMlroseTsp import GeneticAlgorithmMlroseTsp
from algorithms.greedy_search.GreadySearchTsp import GreedySearchTsp
from algorithms.local_search.LocalSearchTsp import LocalSearchTsp
from algorithms.simulated_annealing.SimulatedAnnealing import SimulatedAnnealingTsp
from builders.PathBuilder import PathBuilder
from constants.AlgNames import *
from constants.ArgNames import *
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
NAME_OF_DATASET_DIR = "dataset"
parser = ArgumentParser()
parser.add_argument(NAME_OF_ALGORITHM, help="name of algorithm to solve TSP problem\n%s" \
                                            % AVAILABLE_ALGORITHM_NAMES, type=str)
parser.add_argument(NUMBER_OF_CITIES, help="number of cities to select correct dir with samples from dataset",
                    type=int)
parser.add_argument(NUMBER_OF_ALL_SAMPLES, help="number of all samples generated for specific number of cities",
                    type=int)
parser.add_argument(NUMBER_OF_SAMPLE, help="number of sample witch contain input TSP data", type=int)
args = parser.parse_args()

NAME_OF_ALGORITHM = args.name_of_algorithm
NUMBER_OF_CITIES = args.number_of_cities
NUMBER_OF_SAMPLES = args.number_of_all_samples
NUMBER_OF_SAMPLE = args.number_of_sample


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


def main():
    name_of_dir_with_samples = PATTERN_TO_DIRECTORY_FROM_DATASET % (NUMBER_OF_SAMPLES, NUMBER_OF_CITIES)
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
    algorithm.solve()
    msg = "best_trace: %s | full_cost: %s" % (algorithm.best_trace, algorithm.full_cost)
    print(msg)


if __name__ == "__main__":
    main()
