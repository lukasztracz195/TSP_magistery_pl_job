import time
import tracemalloc

from pydantic import ConfigError
from sko.GA import GA_TSP
from sko.operators import selection, crossover, mutation

from algorithms import TSP
from algorithms.TSP import Tsp
from collector.DataCollector import DataCollector
from constants.AlgNamesResults.names import GENETIC_ALGORITHM_HEURISTIC_LIB_SCIKIT_OPT_DIR
from constants.MeasurementTimeWithOutputData import *
from constants.algconfig.AlgConfigNames import *
from threads.profiler import CpuProfiler
from constants.CsvColumnNames import *

def valid_config_selection_mode(selection_mode):
    set_selection_mode = {"selection_tournament_faster", "selection_tournament", "selection_roulette_1",
                          "selection_roulette_2"}
    if selection_mode not in set_selection_mode:
        raise ConfigError("Detected wrong type of selection mode: %s", selection_mode)


def valid_config_mutation_mode(mutation_mode):
    set_mutation_mode = {"mutation_TSP_1", "mutation_reverse", "mutation_swap", "transpose"}
    if mutation_mode not in set_mutation_mode:
        raise ConfigError("Detected wrong type of mutation mode: %s", mutation_mode)


def valid_config_crossover_mode(crossover_mode):
    set_crossover_mode = {"crossover_pmx", "crossover_1point", "crossover_2point", "crossover_2point_bit",
                          "crossover_2point_prob"}
    if crossover_mode not in set_crossover_mode:
        raise ConfigError("Detected wrong type of crossover mode mode: %s", crossover_mode)


class GeneticAlgorithmScikitOpt(Tsp):
    def define_necessary_config_name_to_run(self):
        self.necessary_config_names_to_run = [SUFFIX, SIZE_OF_POPULATION, PROBABILITY_OF_MUTATION, MAX_ATTEMPTS,
                                              MAX_ITERATIONS,
                                              SELECTION_MODE, MUTATION_MODE, CROSSOVER_MODE, TOURN_SIZE]

    def inject_configuration(self, dictionary_with_config=None):
        self.config = dictionary_with_config
        valid_config_selection_mode(self.config[CROSSOVER_MODE])
        valid_config_mutation_mode(self.config[MUTATION_MODE])
        valid_config_crossover_mode(self.config[CROSSOVER_MODE])
        self.remove_unnecessary_config()
        self.configured = True

    def __init__(self, ):
        super().__init__()
        self.define_necessary_config_name_to_run()
        self.name = GENETIC_ALGORITHM_HEURISTIC_LIB_SCIKIT_OPT_DIR
        self.ga = None

    def clear_data_before_measurement(self):
        self.ga = GA_TSP(func=self.tsp_input_data.cal_total_distance, n_dim=self.tsp_input_data.number_of_cities,
                         size_pop=self.config[SIZE_OF_POPULATION], max_iter=self.config[MAX_ITERATIONS],
                         prob_mut=self.config[PROBABILITY_OF_MUTATION])
        self.ga.register('selection', self.get_selection_operator(), tourn_size=self.config[TOURN_SIZE]) \
            .register('mutation', self.get_mutation_operator()) \
            .register('crossover', self.get_crossover_operator())

    def start_counting_with_cpu_profiler(self) -> DataCollector:
        self.can_be_run()
        cpu_profiler = CpuProfiler()
        cpu_profiler.start()
        self.best_trace, self.full_cost = self.ga.run()

        cpu_profiler.stop()
        cpu_profiler.join()
        collector = cpu_profiler.get_collector()
        collector.add_data(PARAMETERS, self.config)
        return collector

    def start_counting_with_time(self) -> DataCollector:
        self.can_be_run()
        collector = DataCollector()
        start = time.clock()
        best_state, best_fitness = self.ga.run()
        stop = time.clock()
        best_state = best_state.tolist()
        best_fitness = best_fitness[0]
        best_state = TSP.shuffle_solution_set_start_and_end_node_as_the_same(best_state, 0)
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

        _, _ = self.ga.run()
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

    def get_selection_operator(self):
        selector = {
            "selection_tournament_faster": selection.selection_tournament_faster,
            "selection_tournament": selection.selection_tournament,
            "selection_roulette_1": selection.selection_roulette_1,
            "selection_roulette_2": selection.selection_roulette_2}
        return selector[self.config[SELECTION_MODE]]

    def get_mutation_operator(self):
        selector = {
            "mutation_TSP_1": mutation.mutation_TSP_1,
            "mutation_reverse": mutation.mutation_reverse,
            "mutation_swap": mutation.mutation_swap,
            "transpose": mutation.transpose}
        return selector[self.config[MUTATION_MODE]]

    def get_crossover_operator(self):
        selector = {
            "crossover_pmx": crossover.crossover_pmx,
            "crossover_1point": crossover.crossover_1point,
            "crossover_2point": crossover.crossover_2point,
            "crossover_2point_bit": crossover.crossover_2point_bit,
            "crossover_2point_prob": crossover.crossover_2point_prob}
        return selector[self.config[CROSSOVER_MODE]]
