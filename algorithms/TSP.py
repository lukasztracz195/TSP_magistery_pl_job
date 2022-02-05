import abc
import gc
import tracemalloc

import numpy as np
from pydantic import ConfigError

from collector.DataCollector import DataCollector
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

    def __init__(self):
        self.tsp_input_data = None
        self.config = None
        self.full_cost = 0
        self.best_trace = None
        self.collector = DataCollector()
        self.configured = False
        self.injected_input_data = False
        self.necessary_config_names_to_run = None

    def inject_input_data(self, tsp_input_data):
        self.tsp_input_data = tsp_input_data
        self.injected_input_data = True

    @abc.abstractmethod
    def define_necessary_config_name_to_run(self):
        pass

    @abc.abstractmethod
    def start_counting_with_cpu_profiler(self) -> DataCollector:
        pass

    @abc.abstractmethod
    def start_counting_with_time(self) -> DataCollector:
        pass

    @abc.abstractmethod
    def start_counting_with_time_and_trace_malloc(self) -> DataCollector:
        pass

    @abc.abstractmethod
    def inject_configuration(self, dictionary_with_config=None):
        pass

    def clear_data_before_measurement(self):
        clear_memory_before_measurement()
        self.full_cost = 0
        self.best_trace = None

    def remove_unnecessary_config(self):
        if self.config is not None and self.necessary_config_names_to_run is not None:
            tmp_dict = self.config.copy()
            keys = self.config.keys()
            necessary_keys_as_set = set(self.necessary_config_names_to_run)
            for key in keys:
                if key not in necessary_keys_as_set:
                    del tmp_dict[key]
            self.config = tmp_dict

    def can_be_run(self):
        if self.configured is True:
            if self.injected_input_data is True:
                if self.necessary_config_names_to_run is None and self.config is None:
                    return True
                elif self.necessary_config_names_to_run is None:
                    raise ConfigError(
                        "Algorithm cannot be started because not necessary_config_names_to_run is not initialized")
                else:
                    for config_name in self.necessary_config_names_to_run:
                        if config_name not in self.config:
                            raise ConfigError(
                                "Algorithm cannot be started because not all required config was achievement")
                    return True
            else:
                raise ConfigError("Algorithm cannot be started because not injected input data")
        raise ConfigError("Algorithm cannot be started because was not configured")

    def clear_data_collector(self):
        self.collector.clear()
