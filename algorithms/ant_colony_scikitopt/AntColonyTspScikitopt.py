import time
import tracemalloc
from sko.ACA import ACA_TSP

from algorithms.TSP import Tsp
from collector.DataCollector import DataCollector
from constants.CsvColumnNames import *
from constants.AlgNamesResults.names import ANT_COLONY_TSP_SCIKIT_OPT_DIR
from constants.algconfig.AlgConfigNames import *
from threads.profiler import CpuProfiler


class AntColonyTspScikitopt(Tsp):

    def define_necessary_config_name_to_run(self):
        self.necessary_config_names_to_run = [SIZE_OF_POPULATION, MAX_ITERATIONS, ALPHA, BETA, RHO, SUFFIX]

    def inject_configuration(self, dictionary_with_config=None):
        self.config = dictionary_with_config
        self.remove_unnecessary_config()
        self.configured = True

    def __init__(self):
        super().__init__()
        self.name = ANT_COLONY_TSP_SCIKIT_OPT_DIR
        self.define_necessary_config_name_to_run()
        self.aca = None

    def start_counting_with_cpu_profiler(self) -> DataCollector:
        self.can_be_run()
        cpu_profiler = CpuProfiler()
        self.aca = ACA_TSP(func=self.tsp_input_data.cal_total_distance,
                           n_dim=self.tsp_input_data.number_of_cities,
                           size_pop=self.config[SIZE_OF_POPULATION],
                           max_iter=self.config[MAX_ITERATIONS],
                           distance_matrix=self.tsp_input_data.cost_matrix,
                           alpha=self.config[ALPHA],
                           beta=self.config[BETA],
                           rho=self.config[RHO])
        cpu_profiler.start()
        self.best_trace, self.full_cost = self.aca.run()
        cpu_profiler.stop()
        cpu_profiler.join()
        collector = cpu_profiler.get_collector()
        collector.add_data(PARAMETERS, self.config)
        return collector

    def start_counting_with_time(self) -> DataCollector:
        self.can_be_run()
        collector = DataCollector()
        self.aca = ACA_TSP(func=self.tsp_input_data.cal_total_distance,
                           n_dim=self.tsp_input_data.number_of_cities,
                           size_pop=self.config[SIZE_OF_POPULATION],
                           max_iter=self.config[MAX_ITERATIONS],
                           distance_matrix=self.tsp_input_data.cost_matrix,
                           alpha=self.config[ALPHA],
                           beta=self.config[BETA],
                           rho=self.config[RHO])
        start = time.clock()
        best_state, best_fitness = self.aca.run()
        stop = time.clock()
        best_state = best_state.tolist()
        best_state.append(0)
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
        start = time.clock()
        before_size, before_peak = tracemalloc.get_traced_memory()

        self.aca = ACA_TSP(func=self.tsp_input_data.cal_total_distance,
                           n_dim=self.tsp_input_data.number_of_cities,
                           size_pop=self.config[SIZE_OF_POPULATION],
                           max_iter=self.config[MAX_ITERATIONS],
                           distance_matrix=self.tsp_input_data.cost_matrix,
                           alpha=self.config[ALPHA],
                           beta=self.config[BETA],
                           rho=self.config[RHO])
        _, _ = self.aca.run()
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
