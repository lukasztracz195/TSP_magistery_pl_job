import json
import os

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
    print("path_to_json: ", path_to_json)
    with open(path_to_json) as f:
        data = json.load(f)
    return data


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
