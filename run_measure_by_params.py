import subprocess

from builders.ArgsBuilder import ArgsBuilder
from constants import ArgNames

NUMBER_OF_CITIES = list(range(3, 51))
INDEXES_OF_SAMPLES = list(range(0, 100))
NAMES_OF_ALGORITHMS = ["Astar", "BrutalForceTsp", "DynamicProgramingHeldKarpTsp", "GeneticAlgorithmMlroseTsp",
                       "GreedySearchTsp", "LocalSearchTsp", "SimulatedAnnealingTsp"]
TYPE_OF_MEASUREMENTS = ["CPU", "TIME_AND_DATA", "TIME_AND_MEMORY"]

alg = "Astar"
index_of_sample = 0
n_cites = 8
type_of_measure = "TIME_AND_DATA"
args_builder = ArgsBuilder()
args_builder.add_arg(ArgNames.NAME_OF_ALGORITHM, alg) \
    .add_arg(ArgNames.NUMBER_OF_CITIES, n_cites) \
    .add_arg(ArgNames.NUMBER_OF_SAMPLE, index_of_sample) \
    .add_arg(ArgNames.TYPE_OF_MEASUREMENT, type_of_measure) \
    .add_arg(ArgNames.OVERRIDE_EXIST_MEASURE_RESULTS, True)
args = args_builder.build()

python_file_name_to_execute = "make_meassurement.py"
python_command = "python %s %s" % (python_file_name_to_execute, args)
# print("Execute command: %s" % python_command)
p = subprocess.Popen(python_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
out, err = p.communicate()
if err != b'':
    raise BaseException("Detected exception: %s" % err)
