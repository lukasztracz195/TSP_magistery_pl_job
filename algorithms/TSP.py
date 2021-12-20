import abc
import gc
import tracemalloc

import numpy as np

from input.TspInputData import TspInputData


def shuffle_solution_set_start_and_end_node_as_the_same(best_trace, start_node) -> object:
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


def move_solution_to_start_and_stop_from_the_same_node(best_trace, start_node):
    new_best_trace = []
    if type(best_trace) == np.ndarray:
        new_best_trace = best_trace.tolist()
    if isinstance(best_trace, list):
        new_best_trace = best_trace
    new_best_trace.append(start_node)
    return new_best_trace


def clear_memory_before_measurement():
    gc.collect(generation=0)
    gc.collect(generation=1)
    gc.collect(generation=2)
    tracemalloc.clear_traces()


class Tsp(abc.ABC):

    def __init__(self, tsp_input_data):
        self.tsp_input_data: TspInputData = tsp_input_data
        self.full_cost = 0
        self.best_trace = None
        self.measurement = None

    @abc.abstractmethod
    def solve(self):
        pass

    @abc.abstractmethod
    def start_counting_with_time(self):
        pass

    @abc.abstractmethod
    def start_counting_with_time_and_trace_malloc(self):
        pass

    def clear_data_before_measurement(self):
        clear_memory_before_measurement()
        self.full_cost = 0
        self.best_trace = None
        self.measurement = None
