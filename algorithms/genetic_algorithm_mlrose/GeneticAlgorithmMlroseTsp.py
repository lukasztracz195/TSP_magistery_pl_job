import sys
import time
import tracemalloc

import six

from algorithms import TSP
from collector.DataCollector import DataCollector
from constants.AlgNamesResults.names import GENETIC_ALGORITHM_HEURISTIC_LIB_MLROSE_DIR
from constants.algconfig.AlgConfigNames import *
from constants.CsvColumnNames import *
from threads.profiler import CpuProfiler

sys.modules['sklearn.externals.six'] = six
from mlrose import TravellingSales, TSPOpt, genetic_alg

from algorithms.TSP import Tsp


class GeneticAlgorithmMlroseTsp(Tsp):
    def define_necessary_config_name_to_run(self):
        self.necessary_config_names_to_run = [SUFFIX, SIZE_OF_POPULATION, PROBABILITY_OF_MUTATION, MAX_ATTEMPTS,
                                              MAX_ITERATIONS]

    def inject_configuration(self, dictionary_with_config=None):
        self.config = dictionary_with_config
        self.remove_unnecessary_config()
        self.configured = True

    def __init__(self):
        super().__init__()
        self.define_necessary_config_name_to_run()
        self.fitness_dists = None
        self.problem_fit = None
        self.name = GENETIC_ALGORITHM_HEURISTIC_LIB_MLROSE_DIR
        self.random_state = 2

    def start_counting_with_cpu_profiler(self) -> DataCollector:
        self.can_be_run()
        self.fitness_dists = TravellingSales(distances=self.tsp_input_data.dist_list)
        self.problem_fit = TSPOpt(length=self.tsp_input_data.number_of_cities,
                                  coords=self.tsp_input_data.coord_list, maximize=False)
        cpu_profiler = CpuProfiler()
        cpu_profiler.start()
        self.best_trace, self.full_cost = genetic_alg(self.problem_fit, random_state=self.random_state,
                                                      pop_size=self.config[SIZE_OF_POPULATION],
                                                      mutation_prob=self.config[PROBABILITY_OF_MUTATION],
                                                      max_attempts=self.config[MAX_ATTEMPTS],
                                                      max_iters=self.config[MAX_ITERATIONS])

        cpu_profiler.stop()
        cpu_profiler.join()
        collector = cpu_profiler.get_collector()
        collector.add_data(PARAMETERS, self.config)
        return collector

    def start_counting_with_time(self) -> DataCollector:
        self.can_be_run()
        self.fitness_dists = TravellingSales(distances=self.tsp_input_data.dist_list)
        self.problem_fit = TSPOpt(length=self.tsp_input_data.number_of_cities,
                                  coords=self.tsp_input_data.coord_list, maximize=False)
        collector = DataCollector()
        start = time.clock()
        best_state, best_fitness = genetic_alg(self.problem_fit, random_state=self.random_state,
                                               pop_size=self.config[SIZE_OF_POPULATION],
                                               mutation_prob=self.config[PROBABILITY_OF_MUTATION],
                                               max_attempts=self.config[MAX_ATTEMPTS],
                                               max_iters=self.config[MAX_ITERATIONS])
        stop = time.clock()
        best_state = best_state.tolist()
        best_state = TSP.shuffle_solution_set_start_and_end_node_as_the_same(best_state, 0)
        collector.add_data(TIME_DURATION_IN_SEC, stop - start)
        collector.add_data(FULL_COST, best_fitness)
        collector.add_data(BEST_WAY, best_state)
        collector.add_data(PARAMETERS, self.config)
        return collector

    def start_counting_with_time_and_trace_malloc(self) -> DataCollector:
        self.can_be_run()
        self.fitness_dists = TravellingSales(distances=self.tsp_input_data.dist_list)
        self.problem_fit = TSPOpt(length=self.tsp_input_data.number_of_cities,
                                  coords=self.tsp_input_data.coord_list, maximize=False)
        collector = DataCollector()

        self.clear_data_before_measurement()
        tracemalloc.start()
        start = time.clock()
        before_size, before_peak = tracemalloc.get_traced_memory()

        _, _ = genetic_alg(self.problem_fit, random_state=self.random_state,
                           pop_size=self.config[SIZE_OF_POPULATION],
                           mutation_prob=self.config[PROBABILITY_OF_MUTATION],
                           max_attempts=self.config[MAX_ATTEMPTS],
                           max_iters=self.config[MAX_ITERATIONS])
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
