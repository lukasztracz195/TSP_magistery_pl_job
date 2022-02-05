import time
import tracemalloc

from python_tsp.exact import solve_tsp_dynamic_programming

from algorithms.TSP import Tsp, move_solution_to_start_and_stop_from_the_same_node
from collector.DataCollector import DataCollector
from constants import MeasurementTimeWithOutputData, MeasurementMemory
from constants.AlgNamesResults.names import DYNAMIC_PROGRAMING_EXAC_HELD_KARP_LIB_DIR
from models.tsp_json_measurement import MeasurementForTime, MeasurementForTimeWithMalloc
from threads.profiler import CpuProfiler


class DynamicProgramingHeldKarpTsp(Tsp):
    def define_necessary_config_name_to_run(self):
        self.necessary_config_names_to_run = None

    def inject_configuration(self, dictionary_with_config=None):
        self.config = None
        self.config = True

    def __init__(self):
        super().__init__()
        self.name = DYNAMIC_PROGRAMING_EXAC_HELD_KARP_LIB_DIR
        self.define_necessary_config_name_to_run()

    def start_counting_with_cpu_profiler(self) -> DataCollector:
        self.can_be_run()
        cpu_profiler = CpuProfiler()
        cpu_profiler.start()
        self.best_trace, self.full_cost = solve_tsp_dynamic_programming(self.tsp_input_data.cost_matrix)
        cpu_profiler.stop()
        cpu_profiler.join()
        return cpu_profiler.get_collector()

    def start_counting_with_time(self) -> DataCollector:
        self.can_be_run()
        collector = DataCollector()
        start = time.clock()
        best_state, best_fitness = solve_tsp_dynamic_programming(self.tsp_input_data.cost_matrix)
        stop = time.clock()
        best_state.append(self.tsp_input_data.selected_city_on_start)
        collector.add_data(MeasurementTimeWithOutputData.TIME_DURATION_WITHOUT_MALLOC_IN_SEC, stop - start)
        collector.add_data(MeasurementTimeWithOutputData.FULL_COST, best_fitness)
        collector.add_data(MeasurementTimeWithOutputData.BEST_WAY, best_state)
        return collector

    def start_counting_with_time_and_trace_malloc(self) -> DataCollector:
        self.can_be_run()
        collector = DataCollector()
        tracemalloc.clear_traces()

        tracemalloc.start()
        before_size, before_peak = tracemalloc.get_traced_memory()
        start = time.clock()

        _, _ = solve_tsp_dynamic_programming(self.tsp_input_data.cost_matrix)

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
