import time
import tracemalloc

from python_tsp.heuristics import solve_tsp_local_search

from algorithms.TSP import Tsp, move_solution_to_start_and_stop_from_the_same_node
from collector.DataCollector import DataCollector
from constants.AlgNamesResults.names import LOCAL_SEARCH_HEURISTIC_LIB_PYTHON_TSP_DIR
from constants.algconfig.AlgConfigNames import PERTURBATION_SCHEME, SUFFIX
from threads.profiler import CpuProfiler
from constants.CsvColumnNames import *

def valid_pertrubation_scheme(pertrubation_scheme):
    set_of_pertrubation = {
        "ps1",
        "ps2",
        "ps3",
        "ps4",
        "ps5",
        "ps6",
        "two_opt"}
    if pertrubation_scheme not in set_of_pertrubation:
        raise Exception("Detected wrong value pertrubation scheme %s" % pertrubation_scheme)


class LocalSearchTsp(Tsp):

    def define_necessary_config_name_to_run(self):
        self.necessary_config_names_to_run = [SUFFIX, PERTURBATION_SCHEME]

    def inject_configuration(self, dictionary_with_config=None):
        self.config = dictionary_with_config
        valid_pertrubation_scheme(self.config[PERTURBATION_SCHEME])
        self.remove_unnecessary_config()
        self.configured = True

    def __init__(self):
        super().__init__()
        self.name = LOCAL_SEARCH_HEURISTIC_LIB_PYTHON_TSP_DIR
        self.define_necessary_config_name_to_run()

    def start_counting_with_cpu_profiler(self) -> DataCollector:
        self.can_be_run()
        cpu_profiler = CpuProfiler()
        cpu_profiler.start()
        best_state, self.full_cost = solve_tsp_local_search(self.tsp_input_data.cost_matrix)
        self.best_trace = move_solution_to_start_and_stop_from_the_same_node(best_state, 0)
        cpu_profiler.stop()
        cpu_profiler.join()
        collector = cpu_profiler.get_collector()
        collector.add_data(PARAMETERS, self.config)
        return collector

    def start_counting_with_time(self) -> DataCollector:
        self.can_be_run()
        collector = DataCollector()
        start = time.clock()
        best_state, best_fitness = solve_tsp_local_search(self.tsp_input_data.cost_matrix)
        self.best_trace = move_solution_to_start_and_stop_from_the_same_node(best_state, 0)
        stop = time.clock()

        collector.add_data(TIME_DURATION_IN_SEC, stop - start)
        collector.add_data(FULL_COST, best_fitness)
        collector.add_data(BEST_WAY, self.best_trace)
        collector.add_data(PARAMETERS, self.config)
        return collector

    def start_counting_with_time_and_trace_malloc(self) -> DataCollector:
        self.can_be_run()
        collector = DataCollector()
        self.clear_data_before_measurement()

        tracemalloc.start()

        before_size, before_peak = tracemalloc.get_traced_memory()
        start = time.clock()

        _, _ = solve_tsp_local_search(distance_matrix=self.tsp_input_data.cost_matrix,
                                      perturbation_scheme=self.config[PERTURBATION_SCHEME])

        stop = time.clock()
        after_size, after_peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        collector.add_data(TIME_DURATION_IN_SEC, stop - start)
        collector.add_data(USED_MEMORY_BEFORE_MEASUREMENT_IN_BYTES, before_size)
        collector.add_data(USED_MEMORY_PEAK_BEFORE_MEASUREMENT_IN_BYTES, before_peak)
        collector.add_data(USED_MEMORY_AFTER_MEASUREMENT_IN_BYTES, after_size)
        collector.add_data(USED_MEMORY_PEAK_AFTER_MEASUREMENT_IN_BYTES, after_size)
        collector.add_data(USED_MEMORY_DIFF_BEFORE_AFTER_MEASUREMENT_IN_BYTES,
                           after_size - before_size)
        collector.add_data(USED_MEMORY_PEAK_DIFF_BEFORE_AFTER_MEASUREMENT_IN_BYTES,
                           after_size - before_size)
        collector.add_data(PARAMETERS, self.config)
        return collector
