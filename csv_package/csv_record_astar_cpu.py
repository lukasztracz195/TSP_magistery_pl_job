import numpy as np

from constants.CsvColumnNames import *
from csv_package.csv_abs_record import CsvAbstractRow


class CsvRecordAstarCpu(CsvAbstractRow):
    def __init__(self):
        self.__column_names = [NUMBER_OF_CITIES,
                               INDEX_OF_SAMPLE,
                               NAME_OF_SRC_FILE,
                               TYPE_OF_MEASUREMENT,
                               USED_ALGORITHM,
                               SUFFIX,
                               MIN_UTILIZATION_OF_CPU,
                               AVG_UTILIZATION_OF_CPU,
                               STD_UTILIZATION_OF_CPU,
                               MAX_UTILIZATION_OF_CPU,
                               TIME_DURATION_IN_SEC,
                               ]
        self.__column_names_set = set(self.__column_names)
        self.__set_column_name_set = set()
        self.__record_dict = {
            NUMBER_OF_CITIES: np.nan,
            INDEX_OF_SAMPLE: np.nan,
            NAME_OF_SRC_FILE: "",
            TYPE_OF_MEASUREMENT: "",
            USED_ALGORITHM: "",
            SUFFIX: "",
            MIN_UTILIZATION_OF_CPU: np.nan,
            AVG_UTILIZATION_OF_CPU: np.nan,
            STD_UTILIZATION_OF_CPU: np.nan,
            MAX_UTILIZATION_OF_CPU: np.nan,
            TIME_DURATION_IN_SEC: np.nan,
        }

    def exist_column_name(self, column_name):
        return column_name in self.__column_names_set

    @property
    def column_names(self):
        return self.__column_names

    @property
    def record_dict(self):
        return self.__record_dict

    def set_value(self, column_name, value):
        if column_name in self.__column_names_set:
            self.__record_dict[column_name] = value
            self.__set_column_name_set.add(column_name)

    def set_values_from_dict(self, dictionary_with_data):
        for column_name in self.__column_names:
            if column_name in dictionary_with_data:
                self.__record_dict[column_name] = dictionary_with_data[column_name]

    def not_set_fields(self):
        return self.__column_names_set.difference(self.__set_column_name_set)
