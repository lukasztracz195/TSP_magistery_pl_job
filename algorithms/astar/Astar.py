import sys
import time
import tracemalloc

from pyglet.gl import ConfigException

from algorithms.TSP import Tsp
from algorithms.astar.model.DictionaryFastFindMin import DictionaryFastFindMinMaxInNode
from algorithms.astar.model.Node import Node
from collector.DataCollector import DataCollector
from constants import MeasurementTimeWithOutputData, MeasurementMemory, MeasurementBasic
from constants.AlgNamesResults.names import *
from constants.algconfig.AlgConfigNames import *
from threads.profiler import CpuProfiler


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

    def clear_data_before_measurement(self):
        if self.list_all_cities_numbers is None:
            self.list_all_cities_numbers = list(map(lambda x: x.number_of_city, self.tsp_input_data.list_of_cities))
            self.set_for_all_indexes_of_cities = set(self.list_all_cities_numbers)
            self.dict_city_A_to_city_B_with_minimum_distance = self.init_dict_city_a_to_city_b_with_minimum_distance()
            self.number_of_all_cities = len(self.list_all_cities_numbers)

    def start_counting_with_cpu_profiler(self) -> DataCollector:
        self.can_be_run()
        cpu_profiler = CpuProfiler()
        cpu_profiler.start()
        self.best_trace, self.full_cost = self.find_way()
        cpu_profiler.stop()
        cpu_profiler.join()
        collector = cpu_profiler.get_collector()
        collector.add_data(MeasurementBasic.PARAMETERS, self.config)
        return collector

    def start_counting_with_time(self) -> DataCollector:
        self.can_be_run()
        collector = DataCollector()
        start = time.clock()
        best_state, best_fitness = self.find_way()
        stop = time.clock()

        collector.add_data(MeasurementTimeWithOutputData.TIME_DURATION_WITHOUT_MALLOC_IN_SEC, stop - start)
        collector.add_data(MeasurementTimeWithOutputData.FULL_COST, best_fitness)
        collector.add_data(MeasurementTimeWithOutputData.BEST_WAY, best_state)
        collector.add_data(MeasurementBasic.PARAMETERS, self.config)
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

        collector.add_data(MeasurementMemory.TIME_DURATION_WITH_MALLOC_IS_SEC, stop - start)
        collector.add_data(MeasurementMemory.USED_MEMORY_BEFORE_MEASUREMENT_IN_BYTES, before_size)
        collector.add_data(MeasurementMemory.USED_MEMORY_PEAK_BEFORE_MEASUREMENT_IN_BYTES, before_peak)
        collector.add_data(MeasurementMemory.USED_MEMORY_AFTER_MEASUREMENT_IN_BYTES, after_size)
        collector.add_data(MeasurementMemory.USED_MEMORY_PEAK_AFTER_MEASUREMENT_IN_BYTES, after_size)
        collector.add_data(MeasurementMemory.USED_MEMORY_DIFF_BEFORE_AFTER_MEASUREMENT_IN_BYTES,
                           after_size - before_size)
        collector.add_data(MeasurementMemory.USED_MEMORY_DIFF_PEAK_BEFORE_AFTER_MEASUREMENT_IN_BYTES,
                           after_size - before_size)
        collector.add_data(MeasurementBasic.PARAMETERS, self.config)
        return collector

    # OPTIMAL
    def find_way(self):
        self.last = Node(parent=None, g_value=0.0, h_value=sys.maxsize, index_city=self.start_city_number)
        self.nodes_gh_dict.clear()
        while len(self.last.way) < self.number_of_all_cities:
            set_of_unvisited_nodes = self.generate_set_for_all_unvisited_indexes_of_cities(self.last)
            for unvisited_index_city in set_of_unvisited_nodes:
                distance = self.tsp_input_data.get_distance(self.last.index_city, unvisited_index_city)
                g_value = self.last.g_value + distance
                h_value = self.count_heuristic()
                suggest_node = Node(parent=self.last, g_value=g_value, h_value=h_value, index_city=unvisited_index_city)
                self.nodes_gh_dict.add(suggest_node.gh_value, suggest_node)
            selected_value = self.nodes_gh_dict.get_min_value_of_key()
            selected_node = self.nodes_gh_dict[selected_value]
            if self.nodes_gh_dict.key_exists(selected_value):
                self.nodes_gh_dict.pop(selected_value, selected_node)
                self.last = selected_node
        distance = self.tsp_input_data.get_distance(self.last.index_city, self.start_city_number)
        g_value = self.last.g_value + distance
        h_value = distance
        final_node = Node(parent=self.last, g_value=g_value, h_value=h_value, index_city=self.start_city_number)
        self.last = final_node
        return self.last.way, self.last.g_value

    def count_heuristic(self):
        heuristic_model = str(self.config[HEURISTIC_MODEL])
        if heuristic_model.lower() == "a":
            return self.heuristic_a()
        if heuristic_model.lower() == "b":
            return self.heuristic_b()
        raise ConfigException("Expected heuristic_model A or B but achievement %s" % heuristic_model)

    def heuristic_a(self):
        number_of_unvisited_cities = self.number_of_all_cities - len(self.last.way)
        return self.find_min_distance_in_unvisited_nodes() * number_of_unvisited_cities

    def heuristic_b(self):
        return self.get_sum_distance_unvisited_nodes()

    def generate_set_for_all_unvisited_indexes_of_cities(self, parent):
        temp_set = self.set_for_all_indexes_of_cities.copy()
        to_delete = parent.way
        temp_set.difference_update(to_delete)
        return temp_set

    def find_min_distance_in_unvisited_nodes(self):
        tuple_city_and_distance_min = self.dict_city_A_to_city_B_with_minimum_distance[self.last.index_city]
        return tuple_city_and_distance_min[1]

    def get_sum_distance_unvisited_nodes(self):
        unvisited_indexes_of_cities = self.generate_set_for_all_unvisited_indexes_of_cities(self.last)
        s = 0.0
        for not_visited_city_index in unvisited_indexes_of_cities:
            s += self.dict_city_A_to_city_B_with_minimum_distance[not_visited_city_index][1]
        return s

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
