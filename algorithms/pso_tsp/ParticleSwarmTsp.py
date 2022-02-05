import time
import tracemalloc

from algorithms import TSP
from algorithms.TSP import Tsp
from algorithms.pso_tsp.graph import Graph
from algorithms.pso_tsp.pso import PSO
from collector.DataCollector import DataCollector
from constants import MeasurementTimeWithOutputData, MeasurementMemory, MeasurementBasic
from constants.AlgNamesResults.names import *
from constants.algconfig.AlgConfigNames import *
from threads.profiler import CpuProfiler


class ParticleSwarmTsp(Tsp):
    def define_necessary_config_name_to_run(self):
        self.necessary_config_names_to_run = [SUFFIX, MAX_ITERATIONS, SIZE_OF_POPULATION, ALPHA, BETA]

    def inject_configuration(self, dictionary_with_config=None):
        self.config = dictionary_with_config
        self.remove_unnecessary_config()
        self.configured = True

    def __init__(self):
        super().__init__()
        self.define_necessary_config_name_to_run()
        self.graph = None
        self.name = PARTICLE_SWARM_OPT_TSP_DIR

    def clear_data_before_measurement(self):
        if self.graph is None:
            self.graph = Graph(self.tsp_input_data.number_of_cities)
            tmp_graph = self.tsp_input_data.graph
            for city_A in tmp_graph.keys():
                for city_B in tmp_graph.keys():
                    if city_B in tmp_graph[city_A]:
                        if not self.graph.existsEdge(city_A, city_B):
                            distance = tmp_graph[city_A][city_B]
                            self.graph.addEdge(city_A, city_B, distance)
        self.pso = PSO(self.graph, self.config[MAX_ITERATIONS],
                       self.config[SIZE_OF_POPULATION], self.config[BETA], self.config[ALPHA])

    def start_counting_with_cpu_profiler(self) -> DataCollector:
        self.can_be_run()
        cpu_profiler = CpuProfiler()
        cpu_profiler.start()
        self.pso.run()
        self.best_trace = self.pso.getGBest().getPBest()
        self.full_cost = self.pso.getGBest().getCostPBest()
        cpu_profiler.stop()
        cpu_profiler.join()
        collector = cpu_profiler.get_collector()
        collector.add_data(MeasurementBasic.PARAMETERS, self.config)
        return collector

    def start_counting_with_time(self) -> DataCollector:
        self.can_be_run()
        collector = DataCollector()
        start = time.clock()
        self.pso.run()
        best_state = self.pso.getGBest().getPBest()
        best_fitness = self.pso.getGBest().getCostPBest()
        stop = time.clock()
        best_state = TSP.shuffle_solution_set_start_and_end_node_as_the_same(best_state, 0)

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
        start = time.clock()
        before_size, before_peak = tracemalloc.get_traced_memory()
        self.pso.run()
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
