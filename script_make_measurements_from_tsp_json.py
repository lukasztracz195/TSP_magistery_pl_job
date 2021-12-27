from constants import ArgNames
from builders.ArgsBuilder import ArgsBuilder
from progress.progress import progress_bar
import subprocess
import os


def prepare_output_from_stream(stream_src):
    stream_lines = str(stream_src).split("\\n")
    output = ""
    for stream_line in stream_lines:
        output += stream_line + "\n"
    return output


NUMBER_OF_CITIES = list(range(3, 16))
INDEXES_OF_SAMPLES = list(range(0, 11))
NAMES_OF_ALGORITHMS = ["Astar",
                       "GreedySearchTsp",
                       "LocalSearchTsp",
                       "SimulatedAnnealingTsp",
                       "BrutalForceTsp",
                       "DynamicProgramingHeldKarpTsp",
                       "GeneticAlgorithmMlroseTsp"]
TYPE_OF_MEASUREMENT = ["CPU", "TIME_AND_DATA", "TIME_AND_MEMORY"]
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
                    .add_arg(ArgNames.OVERRIDE_EXIST_MEASURE_RESULTS, False)
                args = args_builder.build()
                python_file_name_to_execute = "make_meassurement.py"
                python_command = "python %s %s" % (python_file_name_to_execute, args)
                # print("Execute command: %s" % python_command)
                p = subprocess.Popen(python_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                out, err = p.communicate()
                if err != b'':
                    stack_trace = prepare_output_from_stream(err)
                    raise BaseException("Detected exception\n %s" % stack_trace)
                current += 1
                measure = "{0:^15s}".format(type_of_measure)
                title = "ALG: %s | N: %d | ns: %d | measure: %s |" % (alg, n_cites, index_of_sample, measure)
                progress_bar(current, total, title)
