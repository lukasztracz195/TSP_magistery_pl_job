import numpy as np


class DataCollector:

    def __init__(self):
        self.dictionary_of_data = dict()

    def add_data(self, key, value):
        self.dictionary_of_data[key] = value

    def add_data_to_list(self, key, value):
        if key not in self.dictionary_of_data:
            self.dictionary_of_data[key] = list()
        self.dictionary_of_data[key].append(value)

    def get_or_nan(self, key):
        if key in self.dictionary_of_data:
            return self.dictionary_of_data[key]
        return np.nan

    def get_or_default_str(self, key):
        if key in self.dictionary_of_data:
            return self.dictionary_of_data[key]
        return "NOT_DEFINED"

    def clear(self):
        self.dictionary_of_data.clear()

    def get_dictionary_with_data(self):
        return self.dictionary_of_data
