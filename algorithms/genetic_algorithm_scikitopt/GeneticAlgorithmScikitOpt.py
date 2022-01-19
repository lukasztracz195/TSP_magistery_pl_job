import time
import tracemalloc

import numpy as np
from sko.GA import GA_TSP

from algorithms import TSP
from algorithms.TSP import Tsp
from collector.DataCollector import DataCollector
from constants import MeasurementTimeWithOutputData, MeasurementMemory
from constants.AlgNamesResults.names import GENETIC_ALGORITHM_HEURISTIC_LIB_SCIKIT_OPT_DIR
from threads.profiler import CpuProfiler
from sko.operators import ranking, selection, crossover, mutation


class GeneticAlgorithmScikitOpt(Tsp):
    def __init__(self, tsp_input_data):
        super().__init__(tsp_input_data=tsp_input_data)
        self.name = GENETIC_ALGORITHM_HEURISTIC_LIB_SCIKIT_OPT_DIR
        self.random_state = 2
        self.size_of_population = 200
        self.probability_of_mutation = 0.1
        self.max_attempts = 10
        self.max_iterations = 100

        def cal_total_distance(routine):
            num_points, = routine.shape
            return sum(
                [self.tsp_input_data.cost_matrix[routine[i % num_points], routine[(i + 1) % num_points]] for i in
                 range(num_points)])

        self.ga = GA_TSP(func=cal_total_distance, n_dim=self.tsp_input_data.number_of_cities,
                         size_pop=self.size_of_population, max_iter=self.max_iterations,
                         prob_mut=self.probability_of_mutation)
        self.ga.register('selection', selection.selection_tournament_faster, tourn_size=10) \
            .register('mutation', mutation.mutation_TSP_1) \
            .register('crossover', crossover.crossover_pmx)

    def start_counting_with_cpu_profiler(self) -> DataCollector:
        cpu_profiler = CpuProfiler()
        cpu_profiler.start()
        self.best_trace, self.full_cost = self.ga.run()

        cpu_profiler.stop()
        cpu_profiler.join()
        return cpu_profiler.get_collector()

    def start_counting_with_time(self) -> DataCollector:
        collector = DataCollector()
        start = time.clock()
        best_state, best_fitness = self.ga.run()
        stop = time.clock()
        best_state = best_state.tolist()
        best_fitness = best_fitness[0]
        best_state = TSP.shuffle_solution_set_start_and_end_node_as_the_same(best_state, 0)
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

        _, _ = self.ga.run()
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
