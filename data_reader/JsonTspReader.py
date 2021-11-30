
import json
import os
PATH_TO_DATASET = "dataset"


def get_json_from_file(name_of_directory, name_of_json_file_with_extension):
    current_path = os.getcwd()
    path_to_json = "%s/%s/%s/%s" % (current_path,PATH_TO_DATASET, name_of_directory, name_of_json_file_with_extension)
    data = None
    with open(path_to_json) as f:
        data = json.load(f)
    return data