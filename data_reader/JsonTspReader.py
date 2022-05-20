import json
import os
import re

from models.City import City

PATH_TO_DATASET = "dataset"
PATH_TO_MEASUREMENTS = "measurements"


def get_json_from_file_from_dataset(name_of_directory, name_of_json_file_with_extension, remove_spaces=True):
    current_path = os.getcwd()
    path_to_json = "%s/%s/%s/%s" % (current_path, PATH_TO_DATASET, name_of_directory, name_of_json_file_with_extension)
    data = None
    if remove_spaces:
        path_to_json.replace(" ", "")
    with open(path_to_json) as f:
        data = json.load(f)
    return data


def read_json_from_path(path_to_json):
    data = None
    with open(path_to_json) as f:
        data = json.load(f)
    return data


def read_cities_from_tsp_lib_file(path_to_tsp_lib_file):
    list_of_cities = []
    city_index = 0
    with open(path_to_tsp_lib_file) as file:
        for line in file.readlines():
            if re.search(r'(\d+[ ]+(\d+)[ ]+(\d+))', line):
                macher = re.search(r'(\d+[ ]+(\d+)[ ]+(\d+))', line)
                x = int(macher.group(2))
                y = int(macher.group(3))
                city = City(number_of_city=city_index, x=x, y=y)
                list_of_cities.append(city)
                city_index += 1
    return list_of_cities


def read_solution_from_tsp_lib_file(path_to_tsp_lib_file):
    solution_indexes = []
    with open(path_to_tsp_lib_file) as file:
        for line in file.readlines():
            if re.search(r'^(\d+)', line):
                macher = re.search(r'^(\d+)', line)
                index_of_city = int(macher.group(1)) - 1
                solution_indexes.append(index_of_city)
    return solution_indexes


def get_json_from_file_from_measurements(name_of_directory_of_algorithm, name_of_directory_with_cities,
                                         name_of_json_file_with_extension):
    current_path = os.getcwd()
    path_to_json = "%s/%s/json/%s/%s/%s" % (
        current_path, PATH_TO_MEASUREMENTS, name_of_directory_of_algorithm, name_of_directory_with_cities,
        name_of_json_file_with_extension)
    data = None
    with open(path_to_json) as f:
        data = json.load(f)
    return data
