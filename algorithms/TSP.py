import abc
import gc
import tracemalloc

import numpy as np
import pandas as pd

from models.City import City
from models.tsp_json_measurement import MeasurementForTime, MeasurementForTimeWithMalloc

CITIES = "cities"
NUMBER_OF_CITY = "number_of_city"
X = "x"
Y = "y"
NUMBER_OF_SET = "number_of_set"
MIN = "min"
MAX = "max"
NUMBER_OF_CITIES = "number_of_cities"
MEDIAN = "median"
AVG = "avg"
STDEV = "stdev"
Q1 = "q1"
Q3 = "q3"
IQR = "iqr"
DISTANCE_MATRIX = "distance_matrix"
STATS = "stats"


class Tsp(abc.ABC):
    list_of_cities = list()
    bytes_in_kilobyte = 1024
    bytes_in_megabyte = bytes_in_kilobyte * 1024
    bytes_in_gigabyte = bytes_in_megabyte * 1024

    def __init__(self, tsp_data_json):
        self.tsp_data_json = tsp_data_json
        self.config_dict = dict()
        self.selected_city_on_start = self.tsp_data_json[CITIES][0][NUMBER_OF_CITY]
        self.list_of_cities = self.init_list_of_cities()
        self.cost_matrix = self._prepare_cost_matrix()
        self.number_of_cities = len(self.tsp_data_json[CITIES])
        self.lower_cost_estimate = self._count_lower_cost_estimate()
        self.list_of_cities = self.init_list_of_cities()
        self.graph = self._prepare_graph()
        self.dist_list = self._prepare_distance_list()
        self.coord_list = self._prepare_coords_list()

    @abc.abstractmethod
    def start_counting_with_time(self) -> MeasurementForTime:
        pass

    @abc.abstractmethod
    def start_counting_with_time_and_trace_malloc(self) -> MeasurementForTimeWithMalloc:
        pass


    def init_list_of_cities(self):
        if self.list_of_cities is not None and len(self.list_of_cities) > 0:
            return self.list_of_cities
        list_of_city = list()
        for city_dict in self.tsp_data_json[CITIES]:
            city = City(number_of_city=city_dict[NUMBER_OF_CITY], x=city_dict[X], y=city_dict[Y])
            list_of_city.append(city)
        return list_of_city

    def _prepare_cost_matrix(self):
        list_of_cities = self.init_list_of_cities()
        number_of_cities = len(self.tsp_data_json[CITIES])
        matrix = np.zeros((number_of_cities, number_of_cities))
        for city_1 in list_of_cities:
            for city_2 in list_of_cities:
                distance = City.count_distance(city_1, city_2)
                matrix[city_1.number_of_city][city_2.number_of_city] = distance
        return matrix

    def _count_lower_cost_estimate(self):
        r = 0
        df_cost_matrix = pd.DataFrame(data=self.cost_matrix.copy())
        df_cost_matrix.replace(0, df_cost_matrix.max().max(), inplace=True)
        min_from_rows = df_cost_matrix.min(axis=1)
        min_from_cols = df_cost_matrix.min(axis=0)
        for i in range(0, self.number_of_cities):
            min_row = min_from_rows[i]
            if min_row > 0:
                df_cost_matrix.loc[i] = df_cost_matrix.loc[i] - min_row
                r = r + min_row
        for i in range(0, self.number_of_cities):
            min_col = min_from_cols[i]
            if min_col > 0:
                df_cost_matrix[i] = df_cost_matrix[i] - min_col
                r = r + min_col
        return r

    def get_distance(self, index_of_city_1, index_of_city_2):
        return self.cost_matrix[index_of_city_1][index_of_city_2]

    def _prepare_graph(self):
        list_of_cities = self.init_list_of_cities()
        graph = dict()
        for city in list_of_cities:
            graph[city.number_of_city] = dict()
        for city_1 in list_of_cities:
            for city_2 in list_of_cities:
                distance = City.count_distance(city_1, city_2)
                if distance > 0:
                    graph[city_1.number_of_city][city_2.number_of_city] = distance
        return graph

    def _prepare_distance_list(self):
        list_of_cities = self.init_list_of_cities()
        dist_list = []
        for city_1 in list_of_cities:
            for city_2 in list_of_cities:
                distance = City.count_distance(city_1, city_2)
                if distance > 0:
                    tuple_item = (city_1.number_of_city, city_2.number_of_city, distance)
                    dist_list.append(tuple_item)
        return dist_list

    def _prepare_coords_list(self):
        list_of_cities = self.init_list_of_cities()
        coord_list = []
        for city in list_of_cities:
            tuple_item = (city.x, city.y)
            coord_list.append(tuple_item)
        return coord_list

    def move_solution_to_start_and_stop_from_the_same_node(self, best_trace, start_node):
        new_best_trace = []
        if type(best_trace) == np.ndarray:
            new_best_trace = best_trace.tolist()
        if isinstance(best_trace, list):
            new_best_trace = best_trace
        new_best_trace.append(start_node)
        return new_best_trace

    def shufle_solution_set_start_and_end_node_as_the_same(self, best_trace, start_node):
        new_best_trace = []
        tmp_best_traces_list = []
        if type(best_trace) == np.ndarray:
            tmp_best_traces_list = best_trace.tolist()
        if isinstance(best_trace, list):
            tmp_best_traces_list = best_trace
        index_of_start_node = tmp_best_traces_list.index(start_node)
        for index in range(index_of_start_node, len(tmp_best_traces_list)):
            new_best_trace.append(tmp_best_traces_list[index])
        for index in range(0, index_of_start_node + 1):
            new_best_trace.append(tmp_best_traces_list[index])
        return new_best_trace

    def count_allocated_memory_from_snapshots(self, before_snapshot, after_snapshot):
        memory_used_in_bytes = 0
        statistic_diff_list = after_snapshot.compare_to(before_snapshot, 'lineno')
        if len(statistic_diff_list) != 0:
            allocated_memory_stats = list(filter(lambda x: x.count_diff == 0 or x.size_diff == 0, statistic_diff_list))
            list_of_all_allocated_bytes = list((map(lambda x: x.size, allocated_memory_stats)))
            if len(list_of_all_allocated_bytes) != 0:
                memory_used_in_bytes = sum(list_of_all_allocated_bytes)
        return memory_used_in_bytes

    def clear_memory_before_measurement(self):
        gc.collect(generation=0)
        gc.collect(generation=1)
        gc.collect(generation=2)
        tracemalloc.clear_traces()