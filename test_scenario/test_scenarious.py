from constants.algconfig.AlgConfigNames import *

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
# PRAWDOPODOBIEŃSTWO MUTACJI 0.0001, 0.01, 0.1
# ILOŚĆ PODEJŚĆ 1,5,10
# LICZBA ITERACJI 100, 200, 300

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


def genetic_mlrose_all_combinations_generate():
    GENETIC_MLROSE_TEST_ALGORITHM = list()
    pattern_suffix = "MLROSE_GA_POP_%d_PM_%s_NR_ATMP_%d_NR_ITER_%d"
    size_population_range = [100]
    probability_of_mutation_range = [0.0001, 0.01, 0.1]
    number_of_attemps_range = [1, 5, 10]
    number_of_iterations_range = [100, 200, 300]
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
