import sys
import time
import tracemalloc

import six

from collector.DataCollector import DataCollector
from constants import MeasurementTimeWithOutputData, MeasurementMemory
from threads.profiler import CpuProfiler

sys.modules['sklearn.externals.six'] = six
from mlrose import TravellingSales, TSPOpt, genetic_alg

from algorithms.TSP import Tsp, move_solution_to_start_and_stop_from_the_same_node, \
    shuffle_solution_set_start_and_end_node_as_the_same
from models.tsp_json_measurement import MeasurementForTime, MeasurementForTimeWithMalloc
import numpy as np


class GeneticAlgorithmMlroseTsp(Tsp):
    def __init__(self, tsp_input_data):
        super().__init__(tsp_input_data=tsp_input_data)
        self.fitness_dists = TravellingSales(distances=self.tsp_input_data.dist_list)
        self.problem_fit = TSPOpt(length=self.tsp_input_data.number_of_cities,
                                  coords=self.tsp_input_data.coord_list, maximize=False)
        self.name = "genetic_algorithm_heuristic_lib_mlrose"
        self.random_state = 2
        self.size_of_population = 200
        self.probability_of_mutation = 0.1
        self.max_attempts = 10
        self.max_iterations = np.inf

    def start_counting_with_cpu_profiler(self) -> DataCollector:
        cpu_profiler = CpuProfiler()
        cpu_profiler.start()
        self.best_trace, self.full_cost = genetic_alg(self.problem_fit, random_state=self.random_state,
                                                      pop_size=self.size_of_population,
                                                      mutation_prob=self.probability_of_mutation,
                                                      max_attempts=self.max_attempts,
                                                      max_iters=self.max_iterations)

        cpu_profiler.stop()
        return cpu_profiler.get_collector()

    def start_counting_with_time(self) -> DataCollector:
        collector = DataCollector()
        start = time.clock()
        best_state, best_fitness = genetic_alg(self.problem_fit, random_state=self.random_state,
                                               pop_size=self.size_of_population,
                                               mutation_prob=self.probability_of_mutation,
                                               max_attempts=self.max_attempts, max_iters=self.max_iterations)
        stop = time.clock()

        collector.add_data(MeasurementTimeWithOutputData.TIME_DURATION_WITHOUT_MALLOC_IN_SEC, stop - start)
        collector.add_data(MeasurementTimeWithOutputData.FULL_COST, best_fitness)
        collector.add_data(MeasurementTimeWithOutputData.BEST_WAY, best_state)
        return collector

    def start_counting_with_time_and_trace_malloc(self) -> DataCollector:
        collector = DataCollector()

        self.clear_data_before_measurement()
        tracemalloc.start()
        start = time.clock()
        before_size, before_peak = tracemalloc.get_traced_memory()

        best_state, best_fitness = genetic_alg(self.problem_fit, random_state=self.random_state,
                                               pop_size=self.size_of_population,
                                               mutation_prob=self.probability_of_mutation,
                                               max_attempts=self.max_attempts, max_iters=self.max_iterations)
        stop = time.clock()
        after_size, after_peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        collector.add_data(MeasurementMemory.TIME_DURATION_WITH_MALLOC_IS_SEC, stop - start)
        collector.add_data(MeasurementMemory.USED_MEMORY_BEFORE_MEASUREMENT_IN_BYTES, before_size)
        collector.add_data(MeasurementMemory.USED_MEMORY_PEAK_BEFORE_MEASUREMENT_IN_BYTES, before_peak)
        collector.add_data(MeasurementMemory.USED_MEMORY_AFTER_MEASUREMENT_IN_BYTES, after_size)
        collector.add_data(MeasurementMemory.USED_MEMORY_PEAK_AFTER_MEASUREMENT_IN_BYTES, after_size)
        collector.add_data(MeasurementMemory.USED_MEMORY_DIFF_BEFORE_AFTER_MEASUREMENT_IN_BYTES,
                           after_size - before_size)
        collector.add_data(MeasurementMemory.USED_MEMORY_DIFF_PEAK_BEFORE_AFTER_MEASUREMENT_IN_BYTES,
                           after_size - before_size)
        return collector
