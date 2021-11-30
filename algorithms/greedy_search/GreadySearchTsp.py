import time
import tracemalloc

from python_tsp.heuristics import solve_tsp_simulated_annealing

from algorithms.TSP import Tsp
from models.tsp_json_measurement import MeasurementForTime, MeasurementForTimeWithMalloc


class GreedySearchTsp(Tsp):
    def __init__(self, json_tsp):
        super().__init__(tsp_data_json=json_tsp)
        self.name = "greedy_search_heuristic_self_impl"

    def start_counting_with_time(self) -> MeasurementForTime:
        json_model = MeasurementForTime()
        start = time.clock()
        opt_tour = self.nearest_neighbor(self.list_of_cities)
        stop = time.clock()

        json_model.time_duration_in_sec = stop - start
        json_model.full_cost = opt_tour[1]
        json_model.best_trace = self.shufle_solution_set_start_and_end_node_as_the_same(opt_tour[0], 0)
        json_model.name_of_algorithm = self.name
        return json_model

    def start_counting_with_time_and_trace_malloc(self) -> MeasurementForTimeWithMalloc:
        json_model = MeasurementForTimeWithMalloc()
        self.clear_memory_before_measurement()

        tracemalloc.start()
        before_size, before_peak = tracemalloc.get_traced_memory()
        start = time.clock()

        opt_tour = self.nearest_neighbor(self.list_of_cities)

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
        json_model.full_cost = opt_tour[1]
        json_model.best_trace = self.shufle_solution_set_start_and_end_node_as_the_same(opt_tour[0], 0)

        return json_model

    def get_nearest_neighbor(self, i):
        # Start at infinity
        nearest = [0, float("inf")]

        # print '\n cities:' + str(cities)
        for index in range(len(self.list_of_cities)):
            # Skip if looking at itself or looking at a visited node
            if i == index or self.list_of_cities[index].visited is True:
                pass
            # Otherwise calculate distance and update nearest if necessary
            else:
                distance = self.get_distance(i, index)
                # print nearest
                if distance < nearest[1]:
                    nearest = [index, distance]

        # Set nearest to visited and return
        self.list_of_cities[nearest[0]].visited = True
        return nearest

    def nearest_neighbor(self, cities):
        data = []
        tour = [[], 0]
        first = self.get_nearest_neighbor(0)
        data.append(first)
        next = first
        # Get the nearest neighbor and weight for every vertex and append to the list
        for index in range(1, len(cities)):
            cur = self.get_nearest_neighbor(next[0])
            data.append(cur)
            next = cur

        # Once we have the path and weight, split into 2 arrays for ease of use
        for element in data:
            tour[1] += element[1]
            tour[0].append(element[0])
        # Account for weight of last node -> first node to complete the cycle
        tour[1] += self.get_distance(tour[0][-1], tour[0][0])
        # Return the tour
        return tour