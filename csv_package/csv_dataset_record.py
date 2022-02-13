from typing import Iterable, Any, Mapping

import numpy as np

from constants.CsvColumnNames import *
from csv_package.csv_abs_record import CsvAbstractRow


class CsvDatasetRow(CsvAbstractRow):

    def __init__(self):
        self.__column_names = [NUMBER_OF_CITIES,
                               INDEX_OF_SAMPLE,
                               NAME_OF_SRC_FILE,
                               X_MIN,
                               X_AVG,
                               X_STDEV,
                               X_MEDIAN,
                               X_Q1,
                               X_Q3,
                               X_MAX,
                               Y_MIN,
                               Y_AVG,
                               Y_STDEV,
                               Y_MEDIAN,
                               Y_Q1,
                               Y_Q3,
                               Y_MAX,
                               NR_POINTS_IN_Q1,
                               NR_POINTS_IN_Q2,
                               NR_POINTS_IN_Q3,
                               NR_POINTS_IN_Q4,
                               NR_POINTS_AXIS_X_NEG,
                               NR_POINTS_AXIS_X_POS,
                               NR_POINTS_AXIS_Y_NEG,
                               NR_POINTS_AXIS_Y_POS,
                               NR_POINTS_IN_CENTER,
                               DIST_FROM_CENTER_MIN,
                               DIST_FROM_CENTER_AVG,
                               DIST_FROM_CENTER_STDEV,
                               DIST_FROM_CENTER_MEDIAN,
                               DIST_FROM_CENTER_Q1,
                               DIST_FROM_CENTER_Q3,
                               DIST_FROM_CENTER_MAX,
                               DIST_FROM_CENTER_SUM]
        self.__column_names_set = set(self.__column_names)
        self.__set_column_name_set = set()
        self.__record_dict = {
            NUMBER_OF_CITIES: np.nan,
            INDEX_OF_SAMPLE: np.nan,
            NAME_OF_SRC_FILE: "",
            X_MIN: np.nan,
            X_AVG: np.nan,
            X_STDEV: np.nan,
            X_MEDIAN: np.nan,
            X_Q1: np.nan,
            X_Q3: np.nan,
            X_MAX: np.nan,
            Y_MIN: np.nan,
            Y_AVG: np.nan,
            Y_STDEV: np.nan,
            Y_MEDIAN: np.nan,
            Y_Q1: np.nan,
            Y_Q3: np.nan,
            Y_MAX: np.nan,
            NR_POINTS_IN_Q1: 0,
            NR_POINTS_IN_Q2: 0,
            NR_POINTS_IN_Q3: 0,
            NR_POINTS_IN_Q4: 0,
            NR_POINTS_AXIS_X_NEG: 0,
            NR_POINTS_AXIS_X_POS: 0,
            NR_POINTS_AXIS_Y_NEG: 0,
            NR_POINTS_AXIS_Y_POS: 0,
            NR_POINTS_IN_CENTER: 0,
            DIST_FROM_CENTER_MIN: np.nan,
            DIST_FROM_CENTER_AVG: np.nan,
            DIST_FROM_CENTER_STDEV: np.nan,
            DIST_FROM_CENTER_MEDIAN: np.nan,
            DIST_FROM_CENTER_Q1: np.nan,
            DIST_FROM_CENTER_Q3: np.nan,
            DIST_FROM_CENTER_MAX: np.nan,
            DIST_FROM_CENTER_SUM: np.nan
        }

    def exist_column_name(self, column_name) -> bool:
        return column_name in self.__column_names_set

    @property
    def column_names(self) -> Iterable[Any]:
        return self.__column_names

    @property
    def record_dict(self) -> Mapping[str, Any]:
        return self.__record_dict

    def set_value(self, column_name, value):
        if column_name in self.__column_names_set:
            self.__record_dict[column_name] = value
            self.__set_column_name_set.add(column_name)

    def set_values_from_dict(self, dictionary_with_data):
        for column_name in self.__column_names:
            if column_name in dictionary_with_data:
                self.__record_dict[column_name] = dictionary_with_data[column_name]

    def not_set_fields(self) -> Iterable[Any]:
        return self.__column_names_set.difference(self.__set_column_name_set)
