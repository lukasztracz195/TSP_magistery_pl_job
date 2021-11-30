import time
import tracemalloc
import gc
from algorithms.TSP import Tsp
from algorithms.astar.model.Node import Node
from models.tsp_json_measurement import MeasurementForTime, MeasurementForTimeWithMalloc


class Astar(Tsp):
    def __init__(self, tsp_data_json):
        super().__init__(tsp_data_json)
        self.start_city_number = 0
        self.last = None
        self.prio_dict = dict()
        self.name = "astar_heuristic_self_impl"

    def start_counting_with_time(self) -> MeasurementForTime:
        json_model = MeasurementForTime()
        start = time.clock()
        best_state, best_fitness = self.find_way()
        stop = time.clock()

        json_model.time_duration_in_sec = stop - start
        json_model.full_cost = best_fitness
        json_model.best_trace = best_state
        json_model.name_of_algorithm = self.name
        return json_model

    def start_counting_with_time_and_trace_malloc(self) -> MeasurementForTimeWithMalloc:
        json_model = MeasurementForTimeWithMalloc()
        self.clear_memory_before_measurement()

        tracemalloc.start()

        before_size, before_peak = tracemalloc.get_traced_memory()
        start = time.clock()

        best_state, best_fitness = self.find_way()

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
        json_model.best_trace = best_state
        return json_model

    def find_way(self):
        self.prio_dict = dict()
        self.last = Node(None, 0.0, self.start_city_number)
        while len(self.last.way) < len(self.list_of_cities):
            set_of_unvisited_nodes = self.generate_set_for_all_unvisited_indexes_of_cities(self.last)
            for unvisited_index_city in set_of_unvisited_nodes:
                distance = self.get_distance(self.last.index_city, unvisited_index_city)
                heuristic_value = self.find_min_distance_in_unvisited_nodes() * (
                        len(self.list_of_cities) - len(self.last.way))
                a_start_value = self.last.cost + distance + heuristic_value
                suggest_node = Node(self.last, distance, unvisited_index_city)
                self.prio_dict[a_start_value] = suggest_node
                selected_value = min(self.prio_dict.keys())
                selected_node = self.prio_dict[selected_value]
                self.prio_dict.pop(selected_value)
                self.last = selected_node
        final_node = Node(self.last, self.get_distance(self.last.index_city, self.start_city_number),
                          self.start_city_number)
        self.last = final_node
        return self.last.way, self.last.cost

    def generate_set_for_all_indexes_of_cities(self):
        temp_set = set()
        for city in self.list_of_cities:
            temp_set.add(city.number_of_city)
        return temp_set

    def generate_set_for_all_unvisited_indexes_of_cities(self, parent):
        temp_set = self.generate_set_for_all_indexes_of_cities()
        for index_of_city in parent.way:
            temp_set.remove(index_of_city)
        return temp_set

    def count_sum_lowest_distance(self, how_many):
        sum = 0.0
        distance_from_start = list(self.cost_matrix[:, self.start_city_number])
        if len(distance_from_start) > 0:
            for number_of_city in range(1, how_many):
                first_distance = distance_from_start[0]
                sum += first_distance
                distance_from_start.remove(first_distance)
        return sum

    def find_min_distance_in_unvisited_nodes(self):
        set_of_unvisited_index_cities = self.generate_set_for_all_unvisited_indexes_of_cities(self.last)
        min = 0.0
        for index_of_city in set_of_unvisited_index_cities:
            distance_to_probably_new_min = self.get_distance(self.last.index_city, index_of_city)
            if min > distance_to_probably_new_min:
                min = distance_to_probably_new_min
        return min
