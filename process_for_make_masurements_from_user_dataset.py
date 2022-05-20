import multiprocessing
import os
import time
from datetime import timedelta
from multiprocessing import Process, Queue

import pandas as pd
import psutil

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
from constants import CsvColumnNames
from constants.AlgNames import *
from constants.CsvColumnNames import UTILIZATION_OF_CPU, BEST_WAY, \
    HAMILTONIAN_CYCLE_COST, BEST_WAY_IS_OPTIMAL, ABSOLUTE_DISTANCE_ERROR, RELATIVE_DISTANCE_ERROR, OPTIMAL_WAY, \
    OPTIMAL_COST, MIN_UTILIZATION_OF_CPU, AVG_UTILIZATION_OF_CPU, MAX_UTILIZATION_OF_CPU, STD_UTILIZATION_OF_CPU
from constants.FileExtensions import CSV
from constants.MeasurementsTypes import *
from csv_package.csv_manager import CsvManager
from csv_package.csv_record import CsvRecord
from data_reader import JsonTspReader
from input.TspInputData import TspInputData
from metrics.tsp_metrics import TspOptimalVerifier
from progress.progress import progress_bar
from test_scenario.test_scenarious import *

NAME_OF_DATASET_DIR = "dataset"
PATTERN_TO_DIRECTORY_FROM_DATASET = "TSP_DIST_%d_N_%d"
PATTERN_TO_FILE_NAME_OF_SAMPLE = "TSP_CITIES_SET_%d_N_%d.json"
PATTERN_TO_OUTPUT_DIRECTORY_FROM_NAME_OF_SAMPLE = "TSP_MEASUREMENTS_FROM_SET_%d_N_%d"


def print_diff_time(diff_time_in_sec):
    return "{:0>8}".format(str(timedelta(seconds=int(diff_time_in_sec))))


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


def set_priority(pid=None, priority=1):
    """ Set The Priority of a Windows Process.  Priority is a value between 0-5 where
        2 is normal priority.  Default sets the priority of the current
        python process but can take any valid process ID. """

    import win32api, win32process, win32con

    priority_classes = [win32process.IDLE_PRIORITY_CLASS,
                        win32process.BELOW_NORMAL_PRIORITY_CLASS,
                        win32process.NORMAL_PRIORITY_CLASS,
                        win32process.ABOVE_NORMAL_PRIORITY_CLASS,
                        win32process.HIGH_PRIORITY_CLASS,
                        win32process.REALTIME_PRIORITY_CLASS]
    if pid is None:
        pid = win32api.GetCurrentProcessId()
    handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, pid)
    win32process.SetPriorityClass(handle, priority_classes[priority])


def dictionary_to_str(dictionary):
    content = ""
    for key in dictionary:
        content += "%s=%s " % (key, dictionary[key])
    return content


def wait_on_signal(queue):
    while True:
        if queue.get() == "START":
            break


def measure_cpu(cpu_utilization_queue, cpu_profiler_msg_proc_queue, measure_msg_queue, pid_for_tracking):
    wait_on_signal(cpu_profiler_msg_proc_queue)
    p = psutil.Process(pid_for_tracking)
    p.nice(psutil.REALTIME_PRIORITY_CLASS)
    set_priority(pid=os.getpid(), priority=5)
    if pid_for_tracking is not None:
        skipped_first = False
        measure_msg_queue.put("START")
        while psutil.pid_exists(pid_for_tracking):
            try:
                value = p.cpu_percent(interval=0.1)
                if not skipped_first:
                    skipped_first = True
                    continue
                cpu_utilization_queue.put(value)
            except psutil.NoSuchProcess:
                break


def run_measure(algorithm, queue_messages_for_measure, return_dict):
    wait_on_signal(queue_messages_for_measure)
    set_priority(pid=os.getpid(), priority=5)
    collector = algorithm.start_counting_with_time()
    return_dict["DATA"] = collector


def process_for_synchronization_measure(algorithm):
    cpu_utilization_queue = Queue()
    cpu_profiler_msg_proc_queue = Queue()
    measure_msg_queue = Queue()
    manager = multiprocessing.Manager()
    shared_dictionary = manager.dict()
    measure_proc = Process(target=run_measure, args=(algorithm, measure_msg_queue, shared_dictionary))
    measure_proc.start()
    profiler_cpu_proc = Process(target=measure_cpu,
                                args=(cpu_utilization_queue, cpu_profiler_msg_proc_queue, measure_msg_queue,
                                      measure_proc.pid))
    profiler_cpu_proc.start()
    cpu_profiler_msg_proc_queue.put("START")
    profiler_cpu_proc.join()
    measure_proc.join()
    tmp_collector = shared_dictionary["DATA"]
    cpu_utilization_list = list()
    while not cpu_utilization_queue.empty():
        cpu_utilization_list.append(cpu_utilization_queue.get())
    tmp_collector.add_data(UTILIZATION_OF_CPU, cpu_utilization_list)
    return {"DATA": tmp_collector}


def make_measurement(type_measurement, algorithm):
    return_dict = {}
    if type_measurement == TIME_AND_DATA:
        return_dict = process_for_synchronization_measure(algorithm)
        collector = return_dict["DATA"]
        if len(collector.dictionary_of_data[UTILIZATION_OF_CPU]) == 0:
            collector.dictionary_of_data[UTILIZATION_OF_CPU] = [0.0]
        series = pd.Series(collector.dictionary_of_data[UTILIZATION_OF_CPU])
        collector.dictionary_of_data[MIN_UTILIZATION_OF_CPU] = series.min()
        collector.dictionary_of_data[AVG_UTILIZATION_OF_CPU] = series.mean()
        collector.dictionary_of_data[MAX_UTILIZATION_OF_CPU] = series.max()
        collector.dictionary_of_data[STD_UTILIZATION_OF_CPU] = series.std()
        return_dict.update(collector.get_dictionary_with_data())
    if type_measurement == TIME_AND_MEMORY:
        collector = algorithm.start_counting_with_time_and_trace_malloc()
        return_dict.update(collector.get_dictionary_with_data())
    return return_dict


NUMBER_OF_CITIES = list(range(4, 16))

INDEXES_OF_SAMPLES = list(range(0, 100))
# INDEXES_OF_SAMPLES = [0]
NAMES_OF_ALGORITHMS = [
    # ASTAR,
    GREEDY_SEARCH,
    # LOCAL_SEARCH,
    # SIMULATED_ANNEALING,
    # BRUTAL_FORCE,
    # DYNAMIC_PROGRAMING_HELD_KARP  # N15 ns61,
    # GENETIC_ALGORITHM_MLROSE,
    # GENETIC_ALGORITHM_SCIKIT_OPT,
    # PARTICLE_SWARM_TSP,
    # ANT_COLONY_TSP
]
# aco_rho_from_0_1_to_0_9_pop_100_a_1_b_2_max_iter_20
# lenovo y700 = PC1
# company_leptop = PC2
NAME_OF_DIR_FOR_MEASUREMENTS = "MEASURE_DATA/PC1_GREEDY_SEARCH"
CONFIGURATION_LIST_OF_DICT = [{
    SUFFIX: "GREEDY_SEARCH",
}]

# CONFIGURATION_LIST_OF_DICT = aco_combination_generate()

TYPE_OF_MEASUREMENT = [TIME_AND_DATA, TIME_AND_MEMORY]


def measure_sequence():
    total = len(NUMBER_OF_CITIES) * len(INDEXES_OF_SAMPLES) * len(NAMES_OF_ALGORITHMS) * len(
        CONFIGURATION_LIST_OF_DICT) * len(TYPE_OF_MEASUREMENT)
    current = 0
    start = time.time()
    for alg in NAMES_OF_ALGORITHMS:
        for n_cites in NUMBER_OF_CITIES:
            for index_of_sample in INDEXES_OF_SAMPLES:
                for config_dict in CONFIGURATION_LIST_OF_DICT:
                    for type_of_measure in TYPE_OF_MEASUREMENT:
                        name_of_file_name_sample = PATTERN_TO_FILE_NAME_OF_SAMPLE % (index_of_sample, n_cites)
                        name_of_dir_with_samples = PATTERN_TO_DIRECTORY_FROM_DATASET % (1000, n_cites)
                        path_to_sample = PathBuilder() \
                            .add_dir(NAME_OF_DATASET_DIR) \
                            .add_dir(name_of_dir_with_samples) \
                            .add_file_with_extension(name_of_file_name_sample) \
                            .build()
                        path_to_output_csv = PathBuilder() \
                            .add_dir(NAME_OF_DIR_FOR_MEASUREMENTS) \
                            .create_directory_if_not_exists() \
                            .add_file("%s_%s" % (type_of_measure, config_dict[SUFFIX]), CSV) \
                            .build()
                        csv_manager = CsvManager(path_to_csv=path_to_output_csv)
                        json_data = JsonTspReader.read_json_from_path(path_to_sample)
                        tsp_input_data = TspInputData(json_data)
                        algorithm = prepare_algorithm(alg)
                        algorithm.inject_input_data(tsp_input_data)
                        algorithm.inject_configuration(config_dict)
                        algorithm.clear_data_before_measurement()
                        shared_dictionary = make_measurement(type_measurement=type_of_measure, algorithm=algorithm)
                        collector = DataCollector()
                        collector.dictionary_of_data = shared_dictionary
                        collector.add_data(CsvColumnNames.NUMBER_OF_CITIES, n_cites)
                        collector.add_data(CsvColumnNames.INDEX_OF_SAMPLE, index_of_sample)
                        collector.add_data(CsvColumnNames.TYPE_OF_MEASUREMENT, type_of_measure)
                        collector.add_data(CsvColumnNames.USED_ALGORITHM, alg)
                        collector.add_data(CsvColumnNames.NAME_OF_SRC_FILE, name_of_file_name_sample)
                        collector.add_data(CsvColumnNames.SUFFIX, config_dict[SUFFIX])
                        if BEST_WAY in collector.get_dictionary_with_data():
                            if not tsp_input_data.is_valid_way_for_any_type(
                                    collector.get_dictionary_with_data()[BEST_WAY]):
                                best_way = collector.get_dictionary_with_data()[BEST_WAY]
                                raise Exception("Detected wrong generated way for implementation of ",
                                                alg,
                                                " : ", best_way)
                            else:
                                collector.add_data(HAMILTONIAN_CYCLE_COST,
                                                   tsp_input_data.cal_total_distance(
                                                       collector.get_dictionary_with_data()[BEST_WAY]))
                                tsp_optimal_verifier = TspOptimalVerifier(src_tsp_file_name=name_of_file_name_sample,
                                                                          tsp_path_to_verify=
                                                                          collector.get_dictionary_with_data()[
                                                                              BEST_WAY],
                                                                          tsp_cost_to_verify=
                                                                          collector.get_dictionary_with_data()[
                                                                              HAMILTONIAN_CYCLE_COST],
                                                                          tsp_input_data_object=tsp_input_data,
                                                                          is_tsp_lib=False)
                                collector.add_data(BEST_WAY_IS_OPTIMAL, tsp_optimal_verifier.is_optimal_way)
                                collector.add_data(ABSOLUTE_DISTANCE_ERROR,
                                                   tsp_optimal_verifier.absolute_distance_error)
                                collector.add_data(RELATIVE_DISTANCE_ERROR,
                                                   tsp_optimal_verifier.relative_distance_error)
                                collector.add_data(RELATIVE_DISTANCE_ERROR,
                                                   tsp_optimal_verifier.relative_distance_error)
                                collector.add_data(OPTIMAL_WAY, tsp_optimal_verifier.optimal_way)
                                collector.add_data(OPTIMAL_COST, tsp_optimal_verifier.optimal_cost)
                        csv_record = CsvRecord()
                        csv_record.set_values_from_dict(collector.get_dictionary_with_data())
                        csv_manager.append_row_to_file(csv_record)
                        current += 1
                        measure = "{0:^15s}".format(type_of_measure)
                        diff = time.time() - start
                        title = "ALG: %s | N: %d | ns: %d | measure: %s | suffix: %s | time_duration: %s" % (
                            alg, n_cites, index_of_sample, measure, config_dict[SUFFIX], print_diff_time(diff))
                        progress_bar(current, total, title)


if __name__ == "__main__":
    measure_sequence()
