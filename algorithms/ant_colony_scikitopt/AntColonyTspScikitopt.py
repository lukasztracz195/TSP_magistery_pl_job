import time
import tracemalloc

from sko.ACA import ACA_TSP

from algorithms.TSP import Tsp
from collector.DataCollector import DataCollector
from constants import MeasurementTimeWithOutputData, MeasurementMemory
from constants.AlgNamesResults.names import ANT_COLONY_TSP_SCIKIT_OPT_DIR
from threads.profiler import CpuProfiler


class AntColonyTspScikitopt(Tsp):

    def __init__(self, tsp_input_data):
        super().__init__(tsp_input_data)
        self.distance_matrix = self.tsp_input_data.cost_matrix
        self.name = ANT_COLONY_TSP_SCIKIT_OPT_DIR
        self.aca = None
        self.size_pop = 200
        self.max_iter = 100

    def start_counting_with_cpu_profiler(self) -> DataCollector:
        cpu_profiler = CpuProfiler()
        self.aca = ACA_TSP(func=self.tsp_input_data.cal_total_distance, n_dim=self.tsp_input_data.number_of_cities,
                           size_pop=self.size_pop, max_iter=self.max_iter,
                           distance_matrix=self.tsp_input_data.cost_matrix)
        cpu_profiler.start()
        self.best_trace, self.full_cost = self.aca.run()
        cpu_profiler.stop()
        cpu_profiler.join()
        return cpu_profiler.get_collector()

    def start_counting_with_time(self) -> DataCollector:
        collector = DataCollector()
        self.aca = ACA_TSP(func=self.tsp_input_data.cal_total_distance, n_dim=self.tsp_input_data.number_of_cities,
                           size_pop=self.size_pop, max_iter=self.max_iter,
                           distance_matrix=self.tsp_input_data.cost_matrix)
        start = time.clock()
        best_state, best_fitness = self.aca.run()
        stop = time.clock()
        best_state = best_state.tolist()
        best_state.append(0)
        collector.add_data(MeasurementTimeWithOutputData.TIME_DURATION_WITHOUT_MALLOC_IN_SEC, stop - start)
        collector.add_data(MeasurementTimeWithOutputData.FULL_COST, best_fitness)
        collector.add_data(MeasurementTimeWithOutputData.BEST_WAY, best_state)
        return collector

    def start_counting_with_time_and_trace_malloc(self) -> DataCollector:
        collector = DataCollector()

        self.clear_data_before_measurement()
        tracemalloc.start()
        start = time.clock()
        before_size, before_peak = tracemalloc.get_traced_memory()

        self.aca = ACA_TSP(func=self.tsp_input_data.cal_total_distance, n_dim=self.tsp_input_data.number_of_cities,
                           size_pop=self.size_pop, max_iter=self.max_iter,
                           distance_matrix=self.tsp_input_data.cost_matrix)
        best_state, best_fitness = self.aca.run()
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
