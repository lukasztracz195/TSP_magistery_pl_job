import sys
import time
import tracemalloc

from algorithms.TSP import Tsp
from algorithms.astar.model.Node import Node
from collector.DataCollector import DataCollector
from constants import MeasurementTimeWithOutputData, MeasurementMemory
from constants.AlgNamesResults.names import ASTAR_HEURISTIC_SELF_IMPL_DIR
from models.tsp_json_measurement import MeasurementForTime, MeasurementForTimeWithMalloc
from threads.profiler import CpuProfiler


class Astar(Tsp):
    def __init__(self, tsp_data_input):
        super().__init__(tsp_data_input)
        self.start_city_number = 0
        self.last = None
        self.name = ASTAR_HEURISTIC_SELF_IMPL_DIR
        self.list_all_cities_numbers = list(map(lambda x: x.number_of_city, self.tsp_input_data.list_of_cities))
        self.set_for_all_indexes_of_cities = set(self.list_all_cities_numbers)
        self.dict_city_A_to_city_B_with_minimum_distance = self.init_dict_city_a_to_city_b_with_minimum_distance()
        self.number_of_all_cities = len(self.list_all_cities_numbers)

    def start_counting_with_cpu_profiler(self) -> DataCollector:
        cpu_profiler = CpuProfiler()
        cpu_profiler.start()
        self.best_trace, self.full_cost = self.find_way()
        cpu_profiler.stop()
        cpu_profiler.join()
        return cpu_profiler.get_collector()

    def start_counting_with_time(self) -> DataCollector:
        collector = DataCollector()
        start = time.clock()
        best_state, best_fitness = self.find_way()
        stop = time.clock()

        collector.add_data(MeasurementTimeWithOutputData.TIME_DURATION_WITHOUT_MALLOC_IN_SEC, stop - start)
        collector.add_data(MeasurementTimeWithOutputData.FULL_COST, best_fitness)
        collector.add_data(MeasurementTimeWithOutputData.BEST_WAY, best_state)
        return collector

    def start_counting_with_time_and_trace_malloc(self) -> DataCollector:
        collector = DataCollector()
        self.clear_data_before_measurement()

        tracemalloc.start()

        before_size, before_peak = tracemalloc.get_traced_memory()
        start = time.clock()

        _, _ = self.find_way()

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

    def find_way(self):
        self.prio_dict = dict()
        self.last = Node(None, 0.0, self.start_city_number)
        prio_dict = dict()
        while len(self.last.way) < self.number_of_all_cities:
            set_of_unvisited_nodes = self.generate_set_for_all_unvisited_indexes_of_cities(self.last)
            prio_dict = dict()
            for unvisited_index_city in set_of_unvisited_nodes:
                distance = self.tsp_input_data.get_distance(self.last.index_city, unvisited_index_city)
                heuristic_value = self.find_min_distance_in_unvisited_nodes() * (
                        self.number_of_all_cities - len(self.last.way))
                a_start_value = self.last.cost + distance + heuristic_value
                suggest_node = Node(self.last, distance, unvisited_index_city)
                prio_dict[a_start_value] = suggest_node
            selected_value = min(prio_dict.keys())
            selected_node = prio_dict[selected_value]
            self.last = selected_node
        final_node = Node(self.last, self.tsp_input_data.get_distance(self.last.index_city, self.start_city_number),
                          self.start_city_number)
        self.last = final_node
        return self.last.way, self.last.cost

    def generate_set_for_all_unvisited_indexes_of_cities(self, parent):
        temp_set = self.set_for_all_indexes_of_cities.copy()
        to_delete = parent.way
        temp_set.difference_update(to_delete)
        return temp_set

    def count_sum_lowest_distance(self, how_many):
        sum = 0.0
        distance_from_start = list(self.tsp_input_data.cost_matrix[:, self.start_city_number])
        if len(distance_from_start) > 0:
            for number_of_city in range(1, how_many):
                first_distance = distance_from_start[0]
                sum += first_distance
                distance_from_start.remove(first_distance)
        return sum

    def find_min_distance_in_unvisited_nodes(self):
        tuple_city_and_distance_min = self.dict_city_A_to_city_B_with_minimum_distance[self.last.index_city]
        return tuple_city_and_distance_min[1]

    def init_dict_city_a_to_city_b_with_minimum_distance(self):
        tmp = dict()
        for city_A in self.list_all_cities_numbers:
            min = sys.maxsize
            for city_B in self.list_all_cities_numbers:
                if city_A != city_B:
                    distance_to_probably_new_min = self.tsp_input_data.get_distance(city_A, city_B)
                    if min > distance_to_probably_new_min:
                        min = distance_to_probably_new_min
                        tmp[city_A] = (city_B, min)
        return tmp
