import argparse
import json
import re
from argparse import ArgumentParser

from algorithms.ant_colony_scikitopt.AntColonyTspScikitopt import AntColonyTspScikitopt
from algorithms.astar.Astar import Astar
from algorithms.brutalforce.BruteForce import BrutalForceTsp
from algorithms.dynamic_programing_held_karp.DynamicProgramingTsp import DynamicProgramingHeldKarpTsp
from algorithms.genetic_algorithm_mlrose.GeneticAlgorithmMlroseTsp import GeneticAlgorithmMlroseTsp
from algorithms.genetic_algorithm_scikitopt.GeneticAlgorithmScikitOpt import GeneticAlgorithmScikitOpt
from algorithms.greedy_search.GreadySearchTsp import GreedySearchTsp
from algorithms.local_search.LocalSearchTsp import LocalSearchTsp
from algorithms.pso_tsp.ParticleSwarmTsp import ParticleSwarmTsp
from algorithms.simulated_annealing.SimulatedAnnealing import SimulatedAnnealingTsp
from builders.PathBuilder import PathBuilder
from collector.DataCollector import DataCollector
from constants import ArgNames
from constants.AlgNames import *
from constants.AlgNamesResults.names import *
from constants.ArgNames import *
from constants.CsvColumnNames import *
from constants.FileExtensions import CSV
from constants.MeasurementBasic import *
from constants.MeasurementsTypes import *
from csv_package.csv_manager import CsvManager
from csv_package.csv_record import CsvRecord
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
from metrics.tsp_metrics import TspOptimalVerifier


class ParseKwargs(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, dict())
        for value in values:
            key, value = value.split('=')
            getattr(namespace, self.dest)[key] = value


def can_str2int(text):
    list = re.findall(r'\d+', text)
    if len(text) == len(list):
        return True
    return False


def can_str2float(text):
    list = re.findall(r'\d+.\d+', text)
    if len(text) == len(list):
        return True
    return False


def list_of_list_to_dict(list_of_list):
    dictionary = []
    for list_key_value in list_of_list:
        key = list_key_value[0]
        value = list_key_value[1]
        if value.find('.') == -1:
            if can_str2int(value):
                dictionary[key] = int(value)
            else:
                dictionary[key] = value
        else:
            dictionary[key] = float(value)
    return dictionary


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


AVAILABLE_ALGORITHM_NAMES = [ASTAR,
                             BRUTAL_FORCE,
                             DYNAMIC_PROGRAMING_HELD_KARP,
                             GENETIC_ALGORITHM_MLROSE,
                             GREEDY_SEARCH,
                             LOCAL_SEARCH,
                             SIMULATED_ANNEALING]
PATTERN_TO_DIRECTORY_FROM_DATASET = "TSP_DIST_%d_N_%d"
PATTERN_TO_FILE_NAME_OF_SAMPLE = "TSP_CITIES_SET_%d_N_%d.json"
PATTERN_TO_OUTPUT_DIRECTORY_FROM_NAME_OF_SAMPLE = "TSP_MEASUREMENTS_FROM_SET_%d_N_%d"
NAME_OF_DATASET_DIR = "dataset"

parser = ArgumentParser()
parser.add_argument(ArgNames.DIR_OF_MEASUREMENTS,
                    help="name of dir to save results of measurements",
                    type=str)
parser.add_argument(ArgNames.NAME_OF_ALGORITHM,
                    help="name of algorithm to solve TSP problem\n%s" % AVAILABLE_ALGORITHM_NAMES,
                    type=str)
parser.add_argument(ArgNames.NUMBER_OF_CITIES, help="number of cities to select correct dir with samples from dataset",
                    type=int)

parser.add_argument(ArgNames.NUMBER_OF_SAMPLE, help="number of sample witch contain input TSP data", type=int)
parser.add_argument(ArgNames.TYPE_OF_MEASUREMENT, help="type of measurement: CPU, TIME_AND_DATA, TIME_AND_MEMORY",
                    type=str)
parser.add_argument(ArgNames.PARAMETERS_DICTIONARY, dest="dest", nargs='*', action=ParseKwargs,
                    help="dictionary of parameters",
                    type=str)
parser.add_argument(ArgNames.OVERRIDE_EXIST_MEASURE_RESULTS, help="OVERRIDE_EXIST_MEASURE_RESULTS [ True / False ]",
                    type=str2bool, default=False)
args = parser.parse_args()

DISTANCE = 1000
NAME_OF_ALGORITHM_VALUE_FROM_ARGS = args.name_of_algorithm
NUMBER_OF_CITIES_VALUE_FROM_ARGS = args.number_of_cities
NUMBER_OF_SAMPLE_VALUE_FROM_ARGS = args.number_of_sample
TYPE_OF_MEASUREMENT_VALUE_FROM_ARGS = args.type_of_measurement
OVERRIDE_RESULTS = args.override_exist_measure_results
DICTIONARY_OF_PARAMETERS_VALUE_FROM_ARGS = args.dest
DIR_ON_MEASUREMENTS_VALUE_FROM_ARGS = args.dir_of_measurements


def print_dict_debug(dict):
    for key in dict.keys():
        print("key: %s | type: %s   dict[%s]: %s" % (key, type(dict[key]), key, dict[key]))


def get_number_of_city_from_src_name(src_tsp_file):
    numbers = [int(s) for s in re.findall(r'\d+', src_tsp_file)]
    return numbers[1]


def check_valid_way(actual_path_as_str, src_tsp_file):
    actual_path_as_list = json.loads(actual_path_as_str)
    first_node = actual_path_as_list[0]
    number_of_cities = get_number_of_city_from_src_name(src_tsp_file)
    end_node = actual_path_as_list[len(actual_path_as_list) - 1]
    return first_node == end_node and len(actual_path_as_list) == number_of_cities + 1


def prepare_algorithm(name_of_algorithm):
    switcher = {
        ASTAR: Astar(),
        BRUTAL_FORCE: BrutalForceTsp(),
        DYNAMIC_PROGRAMING_HELD_KARP: DynamicProgramingHeldKarpTsp(),
        GENETIC_ALGORITHM_MLROSE: GeneticAlgorithmMlroseTsp(),
        GENETIC_ALGORITHM_SCIKIT_OPT: GeneticAlgorithmScikitOpt(),
        GREEDY_SEARCH: GreedySearchTsp(),
        LOCAL_SEARCH: LocalSearchTsp(),
        SIMULATED_ANNEALING: SimulatedAnnealingTsp(),
        PARTICLE_SWARM_TSP: ParticleSwarmTsp(),
        ANT_COLONY_TSP: AntColonyTspScikitopt()
    }
    return switcher.get(name_of_algorithm, "Invalid name of algorithm")


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


def make_measurement(algorithm) -> DataCollector:
    if TYPE_OF_MEASUREMENT_VALUE_FROM_ARGS == CPU:
        return algorithm.start_counting_with_cpu_profiler()
    if TYPE_OF_MEASUREMENT_VALUE_FROM_ARGS == TIME_AND_DATA:
        return algorithm.start_counting_with_time()
    if TYPE_OF_MEASUREMENT_VALUE_FROM_ARGS == TIME_AND_MEMORY:
        return algorithm.start_counting_with_time_and_trace_malloc()


def main():
    name_of_dir_with_samples = PATTERN_TO_DIRECTORY_FROM_DATASET % (DISTANCE, NUMBER_OF_CITIES_VALUE_FROM_ARGS)
    name_of_file_name_sample = PATTERN_TO_FILE_NAME_OF_SAMPLE % (
        NUMBER_OF_SAMPLE_VALUE_FROM_ARGS, NUMBER_OF_CITIES_VALUE_FROM_ARGS)
    path_to_sample = PathBuilder() \
        .add_dir(NAME_OF_DATASET_DIR) \
        .add_dir(name_of_dir_with_samples) \
        .add_file_with_extension(name_of_file_name_sample) \
        .build()
    path_to_output_csv = PathBuilder() \
        .add_dir(DIR_ON_MEASUREMENTS_VALUE_FROM_ARGS) \
        .create_directory_if_not_exists() \
        .add_file(TYPE_OF_MEASUREMENT_VALUE_FROM_ARGS, CSV) \
        .build()
    csv_manager = CsvManager(path_to_csv=path_to_output_csv)
    json_data = JsonTspReader.read_json_from_path(path_to_sample)
    tsp_input_data = TspInputData(json_data)
    algorithm = prepare_algorithm(NAME_OF_ALGORITHM_VALUE_FROM_ARGS)
    algorithm.inject_input_data(tsp_input_data)
    algorithm.inject_configuration(DICTIONARY_OF_PARAMETERS_VALUE_FROM_ARGS)
    algorithm.clear_data_before_measurement()
    collector = make_measurement(algorithm)
    collector.add_data(NUMBER_OF_CITIES, NUMBER_OF_CITIES_VALUE_FROM_ARGS)
    collector.add_data(INDEX_OF_SAMPLE, NUMBER_OF_SAMPLE_VALUE_FROM_ARGS)
    collector.add_data(TYPE_OF_MEASUREMENT, TYPE_OF_MEASUREMENT_VALUE_FROM_ARGS)
    collector.add_data(USED_ALGORITHM, algorithm.name)
    collector.add_data(NAME_OF_SRC_FILE, name_of_file_name_sample)
    collector.add_data(SUFFIX, DICTIONARY_OF_PARAMETERS_VALUE_FROM_ARGS[SUFFIX])
    if BEST_WAY in collector.get_dictionary_with_data():
        if not tsp_input_data.is_valid_way_for_any_type(collector.get_dictionary_with_data()[BEST_WAY]):
            best_way = collector.get_dictionary_with_data()[BEST_WAY]
            raise Exception("Detected wrong generated way for implementation of ", NAME_OF_ALGORITHM_VALUE_FROM_ARGS,
                            " : ", best_way)
        else:
            collector.add_data(HAMILTONIAN_CYCLE_COST,
                               tsp_input_data.cal_total_distance(collector.get_dictionary_with_data()[BEST_WAY]))
            tsp_optimal_verifier = TspOptimalVerifier(src_tsp_file_name=name_of_file_name_sample,
                                                      tsp_path_to_verify=collector.get_dictionary_with_data()[BEST_WAY],
                                                      tsp_cost_to_verify=collector.get_dictionary_with_data()[
                                                          HAMILTONIAN_CYCLE_COST])
            collector.add_data(BEST_WAY_IS_OPTIMAL, tsp_optimal_verifier.is_optimal_way)
            collector.add_data(ABSOLUTE_DISTANCE_ERROR, tsp_optimal_verifier.absolute_distance_error)
            collector.add_data(RELATIVE_DISTANCE_ERROR, tsp_optimal_verifier.relative_distance_error)
            collector.add_data(RELATIVE_DISTANCE_ERROR, tsp_optimal_verifier.relative_distance_error)
            collector.add_data(OPTIMAL_WAY, tsp_optimal_verifier.optimal_way)
            collector.add_data(OPTIMAL_COST, tsp_optimal_verifier.optimal_cost)
    csv_record = CsvRecord()
    csv_record.set_values_from_dict(collector.get_dictionary_with_data())
    csv_manager.append_row_to_file(csv_record)


if __name__ == "__main__":
    main()
