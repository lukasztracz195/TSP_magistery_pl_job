import time
import tracemalloc

from algorithms.TSP import Tsp, shuffle_solution_set_start_and_end_node_as_the_same
from collector.DataCollector import DataCollector
from constants import MeasurementTimeWithOutputData, MeasurementMemory
from models.tsp_json_measurement import MeasurementForTime, MeasurementForTimeWithMalloc
from threads.profiler import CpuProfiler


class GreedySearchTsp(Tsp):

    def __init__(self, tsp_input_data):
        super().__init__(tsp_input_data=tsp_input_data)
        self.name = "greedy_search_heuristic_self_impl"

    def start_counting_with_cpu_profiler(self) -> DataCollector:
        cpu_profiler = CpuProfiler()
        cpu_profiler.start()
        opt_tour = self.nearest_neighbor(self.tsp_input_data.list_of_cities)
        cpu_profiler.stop()
        self.best_trace = shuffle_solution_set_start_and_end_node_as_the_same(opt_tour[0], 0)
        self.full_cost = opt_tour[1]
        return cpu_profiler.get_collector()

    def start_counting_with_time(self) -> DataCollector:
        collector = DataCollector()
        start = time.clock()
        opt_tour = self.nearest_neighbor(self.tsp_input_data.list_of_cities)
        stop = time.clock()
        self.best_trace = shuffle_solution_set_start_and_end_node_as_the_same(opt_tour[0], 0)
        self.full_cost = opt_tour[1]
        collector.add_data(MeasurementTimeWithOutputData.TIME_DURATION_WITHOUT_MALLOC_IN_SEC, stop - start)
        collector.add_data(MeasurementTimeWithOutputData.FULL_COST, self.full_cost)
        collector.add_data(MeasurementTimeWithOutputData.BEST_WAY, self.best_trace)
        return collector

    def start_counting_with_time_and_trace_malloc(self) -> DataCollector:
        collector = DataCollector()
        self.clear_data_before_measurement()

        tracemalloc.start()
        before_size, before_peak = tracemalloc.get_traced_memory()
        start = time.clock()

        opt_tour = self.nearest_neighbor(self.tsp_input_data.list_of_cities)

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

    def get_nearest_neighbor(self, i):
        # Start at infinity
        nearest = [0, float("inf")]

        # print '\n cities:' + str(cities)
        for index in range(len(self.tsp_input_data.list_of_cities)):
            # Skip if looking at itself or looking at a visited node
            if i == index or self.tsp_input_data.list_of_cities[index].visited is True:
                pass
            # Otherwise calculate distance and update nearest if necessary
            else:
                distance = self.tsp_input_data.get_distance(i, index)
                # print nearest
                if distance < nearest[1]:
                    nearest = [index, distance]

        # Set nearest to visited and return
        self.tsp_input_data.list_of_cities[nearest[0]].visited = True
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
        tour[1] += self.tsp_input_data.get_distance(tour[0][-1], tour[0][0])
        # Return the tour
        return tour
