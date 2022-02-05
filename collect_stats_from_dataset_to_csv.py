import numpy as np
import pandas as pd

from builders.PathBuilder import PathBuilder
from constants.FileExtensions import CSV
from data_reader import JsonTspReader
from functions import exist_file

NUMBER_OF_CITIES = list(range(4, 16))
INDEXES_OF_SAMPLES = list(range(0, 100))
PATTERN_FOR_DIRECTORY_NAME_WITH_SAMPLES = "TSP_DIST_1000_N_%d"
PATTERN_FOR_SAMPLE_NAME = "TSP_CITIES_SET_%d_N_%d.json"
COLUMN_NAMES_IN_CSV_EXISTS_SET = ["number_of_cities", ]
PATTERNS_TO_STATS = ["%s_min", "%s_avg", "%s_stdev", "%s_median", "%s_q1", "%s_q3", "%s_max"]
STATS = ["min", "avg", "stdev", "median", "q1", "q3", "max"]
NAME_FILE = "dataset_stats"
POINTS = ["x", "y"]
CSV_DATA_FRAME = dict()


def add_value_to_list(key, value):
    if key in CSV_DATA_FRAME:
        CSV_DATA_FRAME[key].append(value)
    else:
        CSV_DATA_FRAME[key] = list()


for number_of_city in NUMBER_OF_CITIES:
    for index_of_sample in INDEXES_OF_SAMPLES:
        path_to_dataset_json = PathBuilder() \
            .add_dir("dataset") \
            .add_dir(PATTERN_FOR_DIRECTORY_NAME_WITH_SAMPLES % number_of_city) \
            .add_file_with_extension(PATTERN_FOR_SAMPLE_NAME % (index_of_sample, number_of_city)) \
            .build()
        if exist_file(path_to_dataset_json):
            json_data = JsonTspReader.read_json_from_path(path_to_dataset_json)
            add_value_to_list("number_of_cities", number_of_city)
            add_value_to_list("index_of_sample", index_of_sample)
            for point in POINTS:
                for name_of_stat_without_point_name in STATS:
                    name_stat_with_point_name = "%s_%s" % (point, name_of_stat_without_point_name)
                    add_value_to_list(name_stat_with_point_name,
                                      json_data["stats"][point][name_of_stat_without_point_name])
result_df = pd.DataFrame(CSV_DATA_FRAME)
result_df.replace("", np.nan, inplace=True)
result_df = result_df.dropna()
feature_result_path = PathBuilder() \
    .add_dir("dataset_csv") \
    .create_directory_if_not_exists() \
    .add_file(NAME_FILE, CSV) \
    .build()
result_df.to_csv(feature_result_path)
