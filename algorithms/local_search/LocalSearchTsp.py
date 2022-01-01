import time
import tracemalloc

from python_tsp.heuristics import solve_tsp_local_search

from algorithms.TSP import Tsp, move_solution_to_start_and_stop_from_the_same_node
from collector.DataCollector import DataCollector
from constants import MeasurementTimeWithOutputData, MeasurementMemory
from constants.AlgNamesResults.names import LOCAL_SEARCH_HEURISTIC_LIB_PYTHON_TSP_DIR
from models.tsp_json_measurement import MeasurementForTime, MeasurementForTimeWithMalloc
from threads.profiler import CpuProfiler


class LocalSearchTsp(Tsp):

    def __init__(self, tsp_input_data):
        super().__init__(tsp_input_data=tsp_input_data)
        self.name = LOCAL_SEARCH_HEURISTIC_LIB_PYTHON_TSP_DIR

    def start_counting_with_cpu_profiler(self) -> DataCollector:
        cpu_profiler = CpuProfiler()
        cpu_profiler.start()
        best_state, self.full_cost = solve_tsp_local_search(self.tsp_input_data.cost_matrix)
        self.best_trace = move_solution_to_start_and_stop_from_the_same_node(best_state, 0)
        cpu_profiler.stop()
        cpu_profiler.join()
        return cpu_profiler.get_collector()

    def start_counting_with_time(self) -> DataCollector:
        collector = DataCollector()
        start = time.clock()
        best_state, best_fitness = solve_tsp_local_search(self.tsp_input_data.cost_matrix)
        self.best_trace = move_solution_to_start_and_stop_from_the_same_node(best_state, 0)
        stop = time.clock()

        collector.add_data(MeasurementTimeWithOutputData.TIME_DURATION_WITHOUT_MALLOC_IN_SEC, stop - start)
        collector.add_data(MeasurementTimeWithOutputData.FULL_COST, best_fitness)
        collector.add_data(MeasurementTimeWithOutputData.BEST_WAY, self.best_trace)
        return collector

    def start_counting_with_time_and_trace_malloc(self) -> DataCollector:
        collector = DataCollector()
        self.clear_data_before_measurement()

        tracemalloc.start()

        before_size, before_peak = tracemalloc.get_traced_memory()
        start = time.clock()

        best_state, best_fitness = solve_tsp_local_search(self.tsp_input_data.cost_matrix)

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
