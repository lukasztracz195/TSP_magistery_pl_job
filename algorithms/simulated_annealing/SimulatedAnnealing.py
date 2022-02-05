import time
import tracemalloc

from pydantic import ConfigError
from python_tsp.heuristics import solve_tsp_simulated_annealing

from algorithms.TSP import Tsp, move_solution_to_start_and_stop_from_the_same_node
from collector.DataCollector import DataCollector
from constants import MeasurementTimeWithOutputData, MeasurementMemory, MeasurementBasic
from constants.AlgNamesResults.names import SIMULATED_ANNEALING_HEURISTIC_LIB_PYTHON_TSP_DIR
from constants.algconfig.AlgConfigNames import *
from models.tsp_json_measurement import MeasurementForTime, MeasurementForTimeWithMalloc
from threads.profiler import CpuProfiler


def valid_pertrubation_scheme(pertrubation_scheme):
    set_of_pertrubation = {
        "ps1",
        "ps2",
        "ps3",
        "ps4",
        "ps5",
        "ps6",
        "two_opt"}
    if pertrubation_scheme not in set_of_pertrubation:
        raise ConfigError("Detected wrong value pertrubation scheme %s" % pertrubation_scheme)


class SimulatedAnnealingTsp(Tsp):

    def define_necessary_config_name_to_run(self):
        self.necessary_config_names_to_run = [SUFFIX, PERTURBATION_SCHEME, ALPHA]

    def inject_configuration(self, dictionary_with_config=None):
        self.config = dictionary_with_config
        valid_pertrubation_scheme(self.config[PERTURBATION_SCHEME])
        self.remove_unnecessary_config()
        self.configured = True

    def __init__(self):
        super().__init__()
        self.define_necessary_config_name_to_run()
        self.name = SIMULATED_ANNEALING_HEURISTIC_LIB_PYTHON_TSP_DIR

    def start_counting_with_cpu_profiler(self) -> DataCollector:
        cpu_profiler = CpuProfiler()
        cpu_profiler.start()
        self.best_trace, self.full_cost = solve_tsp_simulated_annealing(distance_matrix=self.tsp_input_data.cost_matrix,
                                                                        perturbation_scheme=self.config[
                                                                            PERTURBATION_SCHEME])
        cpu_profiler.stop()
        cpu_profiler.join()
        collector = cpu_profiler.get_collector()
        collector.add_data(MeasurementBasic.PARAMETERS, self.config)
        return collector

    def start_counting_with_time(self) -> DataCollector:
        collector = DataCollector()

        start = time.clock()
        self.best_trace, self.full_cost = solve_tsp_simulated_annealing(distance_matrix=self.tsp_input_data.cost_matrix,
                                                                        perturbation_scheme=self.config[
                                                                            PERTURBATION_SCHEME])
        self.best_trace = move_solution_to_start_and_stop_from_the_same_node(self.best_trace, 0)
        stop = time.clock()

        collector.add_data(MeasurementTimeWithOutputData.TIME_DURATION_WITHOUT_MALLOC_IN_SEC, stop - start)
        collector.add_data(MeasurementTimeWithOutputData.FULL_COST, self.full_cost)
        collector.add_data(MeasurementTimeWithOutputData.BEST_WAY, self.best_trace)
        collector.add_data(MeasurementBasic.PARAMETERS, self.config)
        return collector

    def start_counting_with_time_and_trace_malloc(self) -> DataCollector:
        collector = DataCollector()
        self.clear_data_before_measurement()

        tracemalloc.start()

        before_size, before_peak = tracemalloc.get_traced_memory()
        start = time.clock()

        self.best_trace, self.full_cost = solve_tsp_simulated_annealing(distance_matrix=self.tsp_input_data.cost_matrix,
                                                                        perturbation_scheme=self.config[
                                                                            PERTURBATION_SCHEME])
        self.best_trace = move_solution_to_start_and_stop_from_the_same_node(self.best_trace, 0)

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
