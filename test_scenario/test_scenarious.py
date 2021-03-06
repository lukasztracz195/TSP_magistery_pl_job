from constants.algconfig.AlgConfigNames import *
import numpy as np

ACO_TEST_1_ON_RHO_RANGE = [
    {SUFFIX: "POP_100_ALFA_1_BETA_2_RHO_0_1_MAX_ITER_20",
     SIZE_OF_POPULATION: 100,
     ALPHA: 1,
     BETA: 2,
     RHO: 0.1,
     MAX_ITERATIONS: 20,
     },
    {SUFFIX: "POP_100_ALFA_1_BETA_2_RHO_0_2_MAX_ITER_20",
     SIZE_OF_POPULATION: 100,
     ALPHA: 1,
     BETA: 2,
     RHO: 0.2,
     MAX_ITERATIONS: 20,
     },
    {SUFFIX: "POP_100_ALFA_1_BETA_2_RHO_0_3_MAX_ITER_20",
     SIZE_OF_POPULATION: 100,
     ALPHA: 1,
     BETA: 2,
     RHO: 0.3,
     MAX_ITERATIONS: 20,
     },
    {SUFFIX: "POP_100_ALFA_1_BETA_2_RHO_0_4_MAX_ITER_20",
     SIZE_OF_POPULATION: 100,
     ALPHA: 1,
     BETA: 2,
     RHO: 0.4,
     MAX_ITERATIONS: 20,
     },
    {SUFFIX: "POP_100_ALFA_1_BETA_2_RHO_0_5_MAX_ITER_20",
     SIZE_OF_POPULATION: 100,
     ALPHA: 1,
     BETA: 2,
     RHO: 0.5,
     MAX_ITERATIONS: 20,
     },
    {SUFFIX: "POP_100_ALFA_1_BETA_2_RHO_0_6_MAX_ITER_20",
     SIZE_OF_POPULATION: 100,
     ALPHA: 1,
     BETA: 2,
     RHO: 0.6,
     MAX_ITERATIONS: 20,
     },
    {SUFFIX: "POP_100_ALFA_1_BETA_2_RHO_0_7_MAX_ITER_20",
     SIZE_OF_POPULATION: 100,
     ALPHA: 1,
     BETA: 2,
     RHO: 0.7,
     MAX_ITERATIONS: 20,
     },
    {SUFFIX: "POP_100_ALFA_1_BETA_2_RHO_0_8_MAX_ITER_20",
     SIZE_OF_POPULATION: 100,
     ALPHA: 1,
     BETA: 2,
     RHO: 0.8,
     MAX_ITERATIONS: 20,
     },
    {SUFFIX: "POP_100_ALFA_1_BETA_2_RHO_0_9_MAX_ITER_20",
     SIZE_OF_POPULATION: 100,
     ALPHA: 1,
     BETA: 2,
     RHO: 0.9,
     MAX_ITERATIONS: 20,
     }
]

ASTAR_TEST = [
    {SUFFIX: 'HEURISTIC_A', HEURISTIC_MODEL: 'A'},
    {SUFFIX: 'HEURISTIC_B', HEURISTIC_MODEL: 'B'},
]
LOCAL_SEARCH_TEST_PERTRUBATION = [
    {SUFFIX: 'ps1', PERTURBATION_SCHEME: 'ps1'},
    {SUFFIX: 'ps2', PERTURBATION_SCHEME: 'ps2'},
    {SUFFIX: 'ps3', PERTURBATION_SCHEME: 'ps3'},
    {SUFFIX: 'ps4', PERTURBATION_SCHEME: 'ps4'},
    {SUFFIX: 'ps5', PERTURBATION_SCHEME: 'ps5'},
    {SUFFIX: 'ps6', PERTURBATION_SCHEME: 'ps6'},
    {SUFFIX: 'two_opt', PERTURBATION_SCHEME: 'two_opt'}
]

GREEDY_SEARCH_TEST = [{SUFFIX: "no_parameters"}]


# POPULACJA 100, 200, 300
# PRAWDOPODOBIE??STWO MUTACJI 0.0001, 0.01, 0.1
# ILO???? PODEJ???? 1,5,10
# LICZBA ITERACJI 100, 200, 300

def float_to_str(number):
    return str(number).replace(".", "_")


def pso_combination_generate():
    PSO_CONFIGURATION = list()
    pattern_suffix = "PSO_POP_%d_ALPHA_%s_BETA_%s_NR_ITER_%d"
    size_population_range = 100
    alpha_range = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    # alpha_range = [ 0.5]
    beta_range = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    # beta_range = [0.5]
    # number_of_iterations_range = [100, 200, 300]
    number_of_iterations_range = [100]
    for alpha in alpha_range:
        for beta in beta_range:
            for num_of_iter in number_of_iterations_range:
                dict_tmp = {
                    SUFFIX: pattern_suffix % (
                        size_population_range, str(alpha).replace(".", "_"), str(beta).replace(".", "_"), num_of_iter),
                    SIZE_OF_POPULATION: size_population_range,
                    ALPHA: alpha,
                    BETA: beta,
                    MAX_ITERATIONS: num_of_iter
                }
                PSO_CONFIGURATION.append(dict_tmp)
    return PSO_CONFIGURATION


def simulated_annealing_combination_generate():
    SIMULATED_ANNEALING_CONFIG_LIST = list()
    pattern_suffix = "SA_ALPHA_%s_PERTURBATION_SCHEME_%s"
    perturbation_scheme = "two_opt"
    alpha_range = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.91, 0.92, 0.93, 0.94, 0.95, 0.96, 0.97, 0.98, 0.99]
    for alpha in alpha_range:
        dict_tmp = {
            SUFFIX: pattern_suffix % (
                str(alpha).replace(".", "_"), perturbation_scheme),
            ALPHA: alpha,
            PERTURBATION_SCHEME: perturbation_scheme,
        }
        SIMULATED_ANNEALING_CONFIG_LIST.append(dict_tmp)
    return SIMULATED_ANNEALING_CONFIG_LIST


def genetic_mlrose_all_combinations_generate():
    GENETIC_MLROSE_TEST_ALGORITHM = list()
    pattern_suffix = "MLROSE_GA_POP_%d_PM_%s_NR_ATMP_%d_NR_ITER_%d"
    size_population_range = [100]
    probability_of_mutation_range = [0.0001, 0.01, 0.1]
    number_of_attemps_range = [5]
    number_of_iterations_range = [100]
    for size_pop in size_population_range:
        for prop_of_mut in probability_of_mutation_range:
            for nr_of_attemps in number_of_attemps_range:
                for num_of_iter in number_of_iterations_range:
                    dict_tmp = {
                        SUFFIX: pattern_suffix % (
                            size_pop, str(prop_of_mut).replace(".", "_"), nr_of_attemps, num_of_iter),
                        SIZE_OF_POPULATION: size_pop,
                        PROBABILITY_OF_MUTATION: prop_of_mut,
                        MAX_ATTEMPTS: nr_of_attemps,
                        MAX_ITERATIONS: num_of_iter
                    }
                    GENETIC_MLROSE_TEST_ALGORITHM.append(dict_tmp)
    return GENETIC_MLROSE_TEST_ALGORITHM


def aco_combination_generate():
    CONFIGURATION = list()
    pattern_suffix = "ACO_POP_%d_ALPHA_%s_BETA_%s_RHO_%s_NR_ITER_%d"
    size_population_range = 100
    alpha_range = list(np.arange(0.1, 2.0, 0.1))
    # alpha_range = [ 0.5]
    rho = 0.7
    beta_range = list(np.arange(0.1, 2.0, 0.1))
    # beta_range = [0.5]
    # number_of_iterations_range = [100, 200, 300]
    number_of_iterations_range = [20]
    for alpha in alpha_range:
        for beta in beta_range:
            for num_of_iter in number_of_iterations_range:
                dict_tmp = {
                    SUFFIX: pattern_suffix % (
                        size_population_range,
                        str(format(alpha, ".1f")).replace(".", "_"),
                        str(format(beta, ".1f")).replace(".", "_"),
                        str(format(rho, ".1f")).replace(".", "_"),
                        num_of_iter),
                    SIZE_OF_POPULATION: size_population_range,
                    ALPHA: alpha,
                    BETA: beta,
                    RHO: rho,
                    MAX_ITERATIONS: num_of_iter
                }
                CONFIGURATION.append(dict_tmp)
    return CONFIGURATION


def scikit_opt_genetic_alg():
    CONFIGURATION = list()
    pattern_suffix = "SCIKIT_AG_POP_%d_PROB_MUT_%s_MAX_ATTEMPTS_%d_NR_ITER_%d"
    prob_mutation_list = [0.001, 0.01, 0.1, 1.0]
    nr_attempts = [1,5,10]
    # nr_attempts = [1]
    max_nr_iteratins = [100,200, 300]
    # max_nr_iteratins = [100]
    size_of_population = 100
    selection_mode = "selection_tournament_faster"
    mutation_mode = "mutation_TSP_1"
    crossover_mode = "crossover_pmx"
    for prob_mut in prob_mutation_list:
        for nr_att in nr_attempts:
            for max_nr_iter in max_nr_iteratins:
                dict_tmp = {
                    SUFFIX: pattern_suffix % (size_of_population,
                                              float_to_str(prob_mut),
                                              nr_att,
                                              max_nr_iter),
                    SIZE_OF_POPULATION: size_of_population,
                    PROBABILITY_OF_MUTATION: prob_mut,
                    MAX_ATTEMPTS: nr_att,
                    MAX_ITERATIONS: max_nr_iter,
                    SELECTION_MODE: selection_mode,
                    MUTATION_MODE: mutation_mode,
                    CROSSOVER_MODE: crossover_mode,
                    TOURN_SIZE: 1
                }
                CONFIGURATION.append(dict_tmp)
    return CONFIGURATION
