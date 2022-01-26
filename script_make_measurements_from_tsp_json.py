from builders.PathBuilder import PathBuilder
from constants import ArgNames
from builders.ArgsBuilder import ArgsBuilder
from constants.AlgNames import *
from constants.MeasurementsTypes import *
from functions import exist_file
from progress.progress import progress_bar
import subprocess
from builders.PathBuilder import PathBuilder


def prepare_output_from_stream(stream_src):
    stream_lines = str(stream_src).split("\\n")
    output = ""
    for stream_line in stream_lines:
        output += stream_line + "\n"
    return output


# NUMBER_OF_CITIES = list(range(4, 16))
NUMBER_OF_CITIES = list(range(14, 16))
# NUMBER_OF_CITIES = [4]
INDEXES_OF_SAMPLES = list(range(0, 1))
# INDEXES_OF_SAMPLES = [0]
NAMES_OF_ALGORITHMS = [
    # ASTAR,
    # GREEDY_SEARCH,
    # LOCAL_SEARCH,
    # SIMULATED_ANNEALING,
    BRUTAL_FORCE,
    # DYNAMIC_PROGRAMING_HELD_KARP  # N15 ns61,
    # GENETIC_ALGORITHM_MLROSE,
    # GENETIC_ALGORITHM_SCIKIT_OPT,
    # PARTICLE_SWARM_TSP,
    # ANT_COLONY_TSP
]
TYPE_OF_MEASUREMENT = [CPU, TIME_AND_DATA, TIME_AND_MEMORY]
# TYPE_OF_MEASUREMENT = [TIME_AND_DATA]
total = len(NUMBER_OF_CITIES) * len(INDEXES_OF_SAMPLES) * len(NAMES_OF_ALGORITHMS) * len(TYPE_OF_MEASUREMENT)
current = 0
for alg in NAMES_OF_ALGORITHMS:
    for n_cites in NUMBER_OF_CITIES:
        for index_of_sample in INDEXES_OF_SAMPLES:
            for type_of_measure in TYPE_OF_MEASUREMENT:
                args_builder = ArgsBuilder()
                args_builder.add_arg(ArgNames.NAME_OF_ALGORITHM, alg) \
                    .add_arg(ArgNames.NUMBER_OF_CITIES, n_cites) \
                    .add_arg(ArgNames.NUMBER_OF_SAMPLE, index_of_sample) \
                    .add_arg(ArgNames.TYPE_OF_MEASUREMENT, type_of_measure) \
                    .add_arg(ArgNames.OVERRIDE_EXIST_MEASURE_RESULTS, "False")
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
                    raise BaseException("Detected exception\n %s" % stack_trace)
                current += 1
                measure = "{0:^15s}".format(type_of_measure)
                title = "ALG: %s | N: %d | ns: %d | measure: %s |" % (alg, n_cites, index_of_sample, measure)
                progress_bar(current, total, title)
