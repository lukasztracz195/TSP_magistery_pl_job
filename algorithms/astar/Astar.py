import sys
import time
import tracemalloc

from constants.CsvColumnNames import *
from algorithms.TSP import Tsp
from algorithms.astar.model.DictionaryFastFindMin import DictionaryFastFindMinMaxInNode
from algorithms.astar.model.Node import Node
from collector.DataCollector import DataCollector
from constants.AlgNamesResults.names import *
from constants.algconfig.AlgConfigNames import *
from threads.profiler import CpuProfiler
import heapq as hq


class Astar(Tsp):

    def define_necessary_config_name_to_run(self):
        self.necessary_config_names_to_run = [HEURISTIC_MODEL, SUFFIX]

    def inject_configuration(self, dictionary_with_config=None):
        self.config = dictionary_with_config
        self.remove_unnecessary_config()
        self.configured = True

    def __init__(self):
        super().__init__()
        self.define_necessary_config_name_to_run()
        self.last = None
        self.nodes_gh_dict = DictionaryFastFindMinMaxInNode()
        self.start_city_number = 0
        self.name = ASTAR_HEURISTIC_SELF_IMPL_DIR
        self.list_all_cities_numbers = None
        self.priority_queue = []

    def clear_data_before_measurement(self):
        if self.list_all_cities_numbers is None:
            self.list_all_cities_numbers = list(map(lambda x: x.number_of_city, self.tsp_input_data.list_of_cities))
            self.set_for_all_indexes_of_cities = set(self.list_all_cities_numbers)
            self.number_of_all_cities = len(self.list_all_cities_numbers)
            self.priority_queue = []

    def start_counting_with_cpu_profiler(self) -> DataCollector:
        self.can_be_run()
        cpu_profiler = CpuProfiler()
        cpu_profiler.start()
        self.best_trace, self.full_cost = self.find_way()
        cpu_profiler.stop()
        cpu_profiler.join()
        collector = cpu_profiler.get_collector()
        collector.add_data(PARAMETERS, self.config)
        return collector

    def start_counting_with_time(self) -> DataCollector:
        self.can_be_run()
        collector = DataCollector()
        start = time.clock()
        best_state, best_fitness = self.find_way()
        stop = time.clock()

        collector.add_data(TIME_DURATION_IN_SEC, stop - start)
        collector.add_data(FULL_COST, best_fitness)
        collector.add_data(BEST_WAY, best_state)
        collector.add_data(PARAMETERS, self.config)
        return collector

    def start_counting_with_time_and_trace_malloc(self) -> DataCollector:
        self.can_be_run()
        collector = DataCollector()
        self.clear_data_before_measurement()

        tracemalloc.start()

        before_size, before_peak = tracemalloc.get_traced_memory()
        start = time.clock()

        _, _ = self.find_way()

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

    def find_way(self):
        first = Node(parent=None, g_value=0.0, h_value=sys.maxsize, index_of_last_visited_city=self.start_city_number)
        set_of_nodes = set()
        set_of_nodes.add(first)
        self.last = first
        while True:
            set_of_unvisited_nodes = self.generate_set_for_all_unvisited_indexes_of_cities()
            for index_city_to_visit in set_of_unvisited_nodes:
                distance = self.tsp_input_data.get_distance(self.last.index_of_last_visited_city, index_city_to_visit)
                g_value = self.last.g_value + distance
                h_value = self.count_heuristic()
                suggest_node = Node(parent=self.last, g_value=g_value, h_value=h_value,
                                    index_of_last_visited_city=index_city_to_visit)
                if suggest_node not in set_of_nodes:
                    set_of_nodes.add(suggest_node)
                    hq.heappush(self.priority_queue, (suggest_node.gh_value, suggest_node))
            selected_node = hq.heappop(self.priority_queue)[1]
            set_of_nodes.remove(selected_node)
            self.last = selected_node
            if len(self.last.way) == self.number_of_all_cities:
                break
        distance = self.tsp_input_data.get_distance(self.last.index_of_last_visited_city, self.start_city_number)
        g_value = self.last.g_value + distance
        h_value = distance
        final_node = Node(parent=self.last, g_value=g_value, h_value=h_value,
                          index_of_last_visited_city=self.start_city_number)
        self.last = final_node
        return self.last.way, self.last.g_value

    def count_heuristic(self):
        heuristic_model = str(self.config[HEURISTIC_MODEL])
        if heuristic_model.lower() == "a":
            return self.heuristic_a()
        if heuristic_model.lower() == "b":
            return self.heuristic_b()
        raise Exception("Expected heuristic_model A or B but achievement %s" % heuristic_model)

    def heuristic_a(self):
        number_of_unvisited_cities = self.number_of_all_cities - (len(self.last.way) + 1)
        return self.find_min_distance_in_unvisited_nodes() * number_of_unvisited_cities

    def heuristic_b(self):
        return self.get_sum_distance_unvisited_nodes()

    def generate_set_for_all_unvisited_indexes_of_cities(self):
        temp_set = self.set_for_all_indexes_of_cities.copy()
        temp_set.difference_update(self.last.way)
        return temp_set

    def find_min_distance_in_unvisited_nodes(self):
        list_tmp = self.get_distances_to_unvisited_nodes()
        if len(list_tmp) == 0:
            return 0
        return min(list_tmp)

    def get_sum_distance_unvisited_nodes(self):
        list_tmp = self.get_distances_to_unvisited_nodes()
        if len(list_tmp) == 0:
            return 0
        return sum(self.get_distances_to_unvisited_nodes())

    def get_distances_to_unvisited_nodes(self):
        set_unvisited_indexes_nodes = self.generate_set_for_all_unvisited_indexes_of_cities()
        distances = list()
        for unvisited_index_node in set_unvisited_indexes_nodes:
            dist = self.tsp_input_data.get_distance(self.last.index_of_last_visited_city, unvisited_index_node)
            distances.append(dist)
        return distances
