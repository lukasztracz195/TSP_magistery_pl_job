import subprocess
import time
from datetime import timedelta

from builders.ArgsBuilder import ArgsBuilder
from builders.PathBuilder import PathBuilder
from constants import ArgNames
from constants.AlgNames import *
from constants.MeasurementsTypes import *
from constants.algconfig.AlgConfigNames import *
from progress.progress import progress_bar
from test_scenario.test_scenarious import *


def prepare_output_from_stream(stream_src):
    stream_lines = str(stream_src).split("\\n")
    output = ""
    for stream_line in stream_lines:
        output += stream_line + "\n"
    return output


def print_diff_time(diff_time_in_sec):
    return "{:0>8}".format(str(timedelta(seconds=int(diff_time_in_sec))))


# ALG: Astar | N: 10 | ns: 36 | measure:  TIME_AND_DATA  | is in progress: [--------->          ] 53.055556 %
NUMBER_OF_CITIES = list(range(4, 16))
# NUMBER_OF_CITIES = list(range(4, 6))
# NUMBER_OF_CITIES = [4]
INDEXES_OF_SAMPLES = list(range(0, 100))
# INDEXES_OF_SAMPLES = [0]
NAMES_OF_ALGORITHMS = [
    # ASTAR,
    # GREEDY_SEARCH,
    # LOCAL_SEARCH,
    # SIMULATED_ANNEALING,
    # BRUTAL_FORCE,
    DYNAMIC_PROGRAMING_HELD_KARP  # N15 ns61,
    # GENETIC_ALGORITHM_MLROSE,
    # GENETIC_ALGORITHM_SCIKIT_OPT,
    # PARTICLE_SWARM_TSP,
    # ANT_COLONY_TSP
]
# aco_rho_from_0_1_to_0_9_pop_100_a_1_b_2_max_iter_20
NAME_OF_DIR_FOR_MEASUREMENTS = "measurements/PC1_brute_force_held_karp"
CONFIGURATION_LIST_OF_DICT = [{
    SUFFIX: "PC1_BRUTE_FORCE_HELD_KARP"
}]


def dictionary_to_str(dictionary):
    content = ""
    for key in dictionary:
        content += "%s=%s " % (key, dictionary[key])
    return content


TYPE_OF_MEASUREMENT = [CPU, TIME_AND_DATA, TIME_AND_MEMORY]
# TYPE_OF_MEASUREMENT = [CPU, TIME_AND_MEMORY]
# TYPE_OF_MEASUREMENT = [TIME_AND_DATA]
total = len(NUMBER_OF_CITIES) * len(INDEXES_OF_SAMPLES) * len(NAMES_OF_ALGORITHMS) * len(
    CONFIGURATION_LIST_OF_DICT) * len(TYPE_OF_MEASUREMENT)
current = 0
start = time.time()
for alg in NAMES_OF_ALGORITHMS:
    for n_cites in NUMBER_OF_CITIES:
        for index_of_sample in INDEXES_OF_SAMPLES:
            for config_dict in CONFIGURATION_LIST_OF_DICT:
                for type_of_measure in TYPE_OF_MEASUREMENT:
                    args_builder = ArgsBuilder()
                    args_builder \
                        .add_arg(ArgNames.DIR_OF_MEASUREMENTS, NAME_OF_DIR_FOR_MEASUREMENTS) \
                        .add_arg(ArgNames.NAME_OF_ALGORITHM, alg) \
                        .add_arg(ArgNames.NUMBER_OF_CITIES, n_cites) \
                        .add_arg(ArgNames.NUMBER_OF_SAMPLE, index_of_sample) \
                        .add_arg(ArgNames.TYPE_OF_MEASUREMENT, type_of_measure) \
                        .add_arg(ArgNames.PARAMETERS_DICTIONARY, dictionary_to_str(config_dict)) \
                        .add_arg(ArgNames.OVERRIDE_EXIST_MEASURE_RESULTS, "True")
                    args = args_builder.build()
                    python_file_name_to_execute = PathBuilder() \
                        .add_file_with_extension("make_meassurement.py") \
                        .build()
                    python_command = "python %s %s" % (python_file_name_to_execute, args)
                    # print("Execute command: %s" % python_command)
                    p = subprocess.Popen(python_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                    out, err = p.communicate()
                    # output = prepare_output_from_stream(out)
                    # print(output)
                    if err != b'':
                        stack_trace = prepare_output_from_stream(err)
                        raise Exception("Detected exception\n %s" % stack_trace)
                    current += 1
                    measure = "{0:^15s}".format(type_of_measure)
                    diff = time.time() - start
                    title = "ALG: %s | N: %d | ns: %d | measure: %s | suffix: %s | time_duration: %s" % (
                        alg, n_cites, index_of_sample, measure, config_dict[SUFFIX], print_diff_time(diff))
                    progress_bar(current, total, title)
