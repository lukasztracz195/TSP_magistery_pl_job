import pandas as pd

from builders.PathBuilder import PathBuilder
from constants.CsvColumnNames import *
from constants.EuklidesPosition import EuclidesPosition
from constants.FileExtensions import CSV
from csv_package.csv_dataset_record import CsvDatasetRow
from csv_package.csv_manager import CsvManager
from data_reader import JsonTspReader
from functions import exist_file
from input.TspInputData import TspInputData

NUMBER_OF_CITIES_LIST = list(range(4, 16))
INDEXES_OF_SAMPLES_LIST = list(range(0, 100))
PATTERN_FOR_DIRECTORY_NAME_WITH_SAMPLES = "TSP_DIST_1000_N_%d"
PATTERN_FOR_SAMPLE_NAME = "TSP_CITIES_SET_%d_N_%d.json"
COLUMN_NAMES_IN_CSV_EXISTS_SET = ["number_of_cities", ]
PATTERNS_TO_STATS = ["%s_min", "%s_avg", "%s_stdev", "%s_median", "%s_q1", "%s_q3", "%s_max"]
STATS = ["min", "avg", "stdev", "median", "q1", "q3", "max"]
POINTS = ["x", "y"]
NAME_FILE = "dataset_stats_v2"
CSV_DATA_FRAME = dict()


def add_value_to_list(key, value):
    if key in CSV_DATA_FRAME:
        CSV_DATA_FRAME[key].append(value)
    else:
        CSV_DATA_FRAME[key] = list()


path_to_output_csv = PathBuilder() \
    .add_dir("dataset_csv") \
    .create_directory_if_not_exists() \
    .add_file(NAME_FILE, CSV) \
    .build()
csv_manager = CsvManager(path_to_output_csv)
for number_of_city in NUMBER_OF_CITIES_LIST:
    for index_of_sample in INDEXES_OF_SAMPLES_LIST:
        csv_dataset_row = CsvDatasetRow()
        path_to_dataset_json = PathBuilder() \
            .add_dir("dataset") \
            .add_dir(PATTERN_FOR_DIRECTORY_NAME_WITH_SAMPLES % number_of_city) \
            .add_file_with_extension(PATTERN_FOR_SAMPLE_NAME % (index_of_sample, number_of_city)) \
            .build()
        if exist_file(path_to_dataset_json):
            json_data = JsonTspReader.read_json_from_path(path_to_dataset_json)
            stats_from_json = json_data["stats"]
            tsp_input_obj = TspInputData(json_data)
            csv_dataset_row.set_value(NUMBER_OF_CITIES, number_of_city)
            csv_dataset_row.set_value(INDEX_OF_SAMPLE, index_of_sample)
            csv_dataset_row.set_value(NAME_OF_SRC_FILE, PATTERN_FOR_SAMPLE_NAME % (index_of_sample, number_of_city))
            for point in POINTS:
                for name_of_stat_without_point_name in STATS:
                    name_stat_with_point_name = "%s_%s" % (point, name_of_stat_without_point_name)
                    csv_dataset_row.set_value(name_stat_with_point_name,
                                              stats_from_json[point][name_of_stat_without_point_name])
            distances_from_center = list()
            for nr_of_city in range(1, tsp_input_obj.number_of_cities):
                distances_from_center.append(tsp_input_obj.get_distance(0, nr_of_city))
            distances_from_center.sort()
            distances_as_series = pd.Series(distances_from_center)
            csv_dataset_row.set_value(DIST_FROM_CENTER_MIN, distances_as_series.min())
            csv_dataset_row.set_value(DIST_FROM_CENTER_AVG, distances_as_series.mean())
            csv_dataset_row.set_value(DIST_FROM_CENTER_STDEV, distances_as_series.std())
            csv_dataset_row.set_value(DIST_FROM_CENTER_MEDIAN, distances_as_series.median())
            csv_dataset_row.set_value(DIST_FROM_CENTER_Q1, distances_as_series.quantile(.25))
            csv_dataset_row.set_value(DIST_FROM_CENTER_Q3, distances_as_series.quantile(.75))
            csv_dataset_row.set_value(DIST_FROM_CENTER_MAX, distances_as_series.max())
            csv_dataset_row.set_value(DIST_FROM_CENTER_SUM, distances_as_series.sum())
            dict_position_points = dict()
            for city in tsp_input_obj.list_of_cities:
                pos_enum = EuclidesPosition.get_position(city.x, city.y)
                switcher = {
                    EuclidesPosition.Q1: NR_POINTS_IN_Q1,
                    EuclidesPosition.Q2: NR_POINTS_IN_Q2,
                    EuclidesPosition.Q3: NR_POINTS_IN_Q3,
                    EuclidesPosition.Q4: NR_POINTS_IN_Q4,
                    EuclidesPosition.AXIS_Y_NEG: NR_POINTS_AXIS_Y_NEG,
                    EuclidesPosition.AXIS_Y_POS: NR_POINTS_AXIS_Y_POS,
                    EuclidesPosition.AXIS_X_NEG: NR_POINTS_AXIS_X_NEG,
                    EuclidesPosition.AXIS_X_POS: NR_POINTS_AXIS_X_POS,
                    EuclidesPosition.CENTER: NR_POINTS_IN_CENTER
                }
                key = switcher[pos_enum]
                if key in dict_position_points:
                    dict_position_points[key] += 1
                else:
                    dict_position_points[key] = 1
            for key_name in dict_position_points:
                csv_dataset_row.set_value(key_name, dict_position_points[key_name])

            csv_manager.append_row_to_file(csv_dataset_row)
