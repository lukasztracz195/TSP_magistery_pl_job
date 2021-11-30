import sys
import time
import tracemalloc

import six

sys.modules['sklearn.externals.six'] = six

import mlrose
from algorithms.TSP import Tsp
from models.tsp_json_measurement import MeasurementForTime, MeasurementForTimeWithMalloc
import numpy as np


class GeneticAlgorithmMlroseTsp(Tsp):
    def __init__(self, json):
        super().__init__(tsp_data_json=json)
        self.fitness_dists = mlrose.TravellingSales(distances=self.dist_list)
        self.problem_fit = mlrose.TSPOpt(length=self.number_of_cities, coords=self.coord_list, maximize=False)
        self.name = "genetic_algorithm_heuristic_lib_mlrose"
        self.random_state = 2
        self.size_of_population = 200
        self.probability_of_mutation = 0.1
        self.max_attempts = 10
        self.max_iterations = np.inf

    def start_counting_with_time(self) -> MeasurementForTime:
        json_model = MeasurementForTime()
        start = time.clock()
        best_state, best_fitness = mlrose.genetic_alg(self.problem_fit, random_state=self.random_state,
                                                      pop_size=self.size_of_population,
                                                      mutation_prob=self.probability_of_mutation,
                                                      max_attempts=self.max_attempts, max_iters=self.max_iterations)
        stop = time.clock()

        json_model.time_duration_in_sec = stop - start
        json_model.full_cost = best_fitness
        json_model.best_trace = self.move_solution_to_start_and_stop_from_the_same_node(best_state, 0)
        json_model.name_of_algorithm = self.name
        return json_model

    def start_counting_with_time_and_trace_malloc(self) -> MeasurementForTimeWithMalloc:
        json_model = MeasurementForTimeWithMalloc()

        self.clear_memory_before_measurement()
        tracemalloc.start()
        start = time.clock()
        before_size, before_peak = tracemalloc.get_traced_memory()

        best_state, best_fitness = mlrose.genetic_alg(self.problem_fit, random_state=self.random_state,
                                                      pop_size=self.size_of_population,
                                                      mutation_prob=self.probability_of_mutation,
                                                      max_attempts=self.max_attempts, max_iters=self.max_iterations)
        stop = time.clock()
        after_size, after_peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        json_model.name_of_algorithm = self.name
        json_model.time_duration_in_sec = stop - start
        json_model.used_memory_before_measurement = before_size
        json_model.used_memory_peak_before_measurement = before_peak
        json_model.used_memory_diff_before_after_measurement = after_size - before_size
        json_model.used_memory_peak_diff_before_after_measurement = after_peak - before_peak
        json_model.used_memory_after_measurement = after_size
        json_model.used_memory_peak_after_measurement = after_peak
        json_model.full_cost = best_fitness
        json_model.best_trace = self.shufle_solution_set_start_and_end_node_as_the_same(best_state, 0)

        return json_model
