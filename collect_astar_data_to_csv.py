from builders.PathBuilder import PathBuilder
from csv_package.csv_manager import CsvManager
from csv_package.csv_record_astar_cpu import CsvRecordAstarCpu
from csv_package.csv_record_astar_data import CsvRecordAstarData
from csv_package.csv_record_astar_memory import CsvRecordAstarMemory
from data_reader import JsonTspReader
from constants.CsvColumnNames import *
import pandas as pd

from functions import exist_file
from input.TspInputData import TspInputData
from metrics.tsp_metrics import TspOptimalVerifier

SUFFIX = "suffix "
NAME_DIR_WITH_MEASUREMENTS = "astar_2_heuristic_measurements"
PATTERN_TO_DICT_WITH_N_MEASUREMENT = "N_%d"
PATTERN_T0_DICT_WITH_SAMPLE_MEASUREMENT = "TSP_MEASUREMENTS_FROM_SET_%d_N_%d"
PATTERN_TO_DICT_WITH_TYME_MEASUREMENT_DIR = "astar_heuristic_self_impl_heuristic_%s"

TYPES_HEURISTICS = ["A", "B"]
TYPE_MEASUREMENTS = ["CPU", "TIME_AND_DATA", "TIME_AND_MEMORY"]

LIST_CSV_RECORDS = list()

path_to_output_file = PathBuilder() \
    .add_dir("measurements") \
    .create_directory_if_not_exists() \
    .add_dir("astar_comapre_heuristics") \
    .create_directory_if_not_exists() \
    .add_file_with_extension("heuristic_B_N_4_15_TIME_AND_MEMORY.csv") \
    .build()
CSV_MANAGER = CsvManager(path_to_output_file)
NUMBER_OF_CITIES_LIST = list(range(4, 16))
INDEXES_OF_SAMPLES_LIST = list(range(0, 11))
HEURISTIC_LIST = ["B"]
TYPE_MEASUREMENT = "TIME_AND_MEMORY"


def get_src_json_from_dataset(n_city, index_sample):
    path_to_src_json = PathBuilder() \
        .add_dir("dataset") \
        .add_dir("TSP_DIST_1000_N_%d" % n_city) \
        .add_file_with_extension("TSP_CITIES_SET_%s_N_%d.json" % (index_sample, n_city)) \
        .build()
    return JsonTspReader.read_json_from_path(path_to_src_json)


def create_row_by_type(type):
    switcher = {
        "CPU": CsvRecordAstarCpu(),
        "TIME_AND_DATA": CsvRecordAstarData(),
        "TIME_AND_MEMORY": CsvRecordAstarMemory()
    }
    return switcher[type]


for n_city in NUMBER_OF_CITIES_LIST:
    for index_sample in INDEXES_OF_SAMPLES_LIST:
        for type_heuristic in HEURISTIC_LIST:
            path_to_src_measurement_json = PathBuilder() \
                .add_dir(NAME_DIR_WITH_MEASUREMENTS) \
                .add_dir("json") \
                .add_dir(PATTERN_TO_DICT_WITH_N_MEASUREMENT % n_city) \
                .add_dir(PATTERN_T0_DICT_WITH_SAMPLE_MEASUREMENT % (index_sample, n_city)) \
                .add_dir(PATTERN_TO_DICT_WITH_TYME_MEASUREMENT_DIR % type_heuristic) \
                .add_file_with_extension("%s.json" % TYPE_MEASUREMENT) \
                .build()
            if exist_file(path_to_src_measurement_json):
                json_data = JsonTspReader.read_json_from_path(path_to_src_measurement_json)
                row = create_row_by_type(TYPE_MEASUREMENT)
                row.set_value(NUMBER_OF_CITIES, n_city)
                row.set_value(INDEX_OF_SAMPLE, index_sample)
                parameters = json_data["parameters"]
                for name_of_field in row.column_names:
                    if name_of_field in json_data:
                        row.set_value(name_of_field, json_data[name_of_field])
                if TYPE_MEASUREMENT == "CPU":
                    row.set_value(TIME_DURATION_IN_SEC, json_data["time_duration_with_cpu_profiler_in_sec"])
                    utilization_of_cpu = json_data["utilization_of_cpu"]
                    row.set_value(SUFFIX, parameters[SUFFIX])
                    cpu_utilization_series = pd.Series(utilization_of_cpu)

                    row.set_value(MIN_UTILIZATION_OF_CPU, cpu_utilization_series.min())
                    row.set_value(AVG_UTILIZATION_OF_CPU, cpu_utilization_series.mean())
                    row.set_value(MAX_UTILIZATION_OF_CPU, cpu_utilization_series.max())
                    row.set_value(STD_UTILIZATION_OF_CPU, cpu_utilization_series.std())
                elif TYPE_MEASUREMENT == "TIME_AND_DATA":
                    json_src_data = get_src_json_from_dataset(n_city, index_sample)
                    tsp_input_obj = TspInputData(json_src_data)
                    row.set_value(SUFFIX, parameters[SUFFIX])
                    row.set_value(TIME_DURATION_IN_SEC, json_data["time_duration_without_malloc_in_sec"])
                    tsp_verifier = TspOptimalVerifier(json_data[NAME_OF_SRC_FILE], json_data[BEST_WAY], json_data[FULL_COST])
                    row.set_value(HAMILTONIAN_CYCLE_COST, tsp_input_obj.cal_total_distance(json_data[BEST_WAY]))
                    row.set_value(BEST_WAY_IS_OPTIMAL, tsp_verifier.is_optimal_way)
                    row.set_value(ABSOLUTE_DISTANCE_ERROR, tsp_verifier.absolute_distance_error)
                    row.set_value(RELATIVE_DISTANCE_ERROR, tsp_verifier.relative_distance_error)
                    row.set_value(OPTIMAL_WAY, tsp_verifier.optimal_way)
                    row.set_value(OPTIMAL_COST, tsp_verifier.optimal_cost)
                elif TYPE_MEASUREMENT == "TIME_AND_MEMORY":
                    row.set_value(TIME_DURATION_IN_SEC, json_data["time_duration_with_malloc_in_sec"])
                CSV_MANAGER.append_row_to_file(row)
