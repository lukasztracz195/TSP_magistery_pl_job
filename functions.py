import os

PATH_TO_DATASET = "dataset"
PATH_TO_MEASUREMENTS = "measurements"


def create_directory_if_not_exists(path):
    if not os.path.exists(path):
        os.mkdir(path)


def exist_file(path):
    return os.path.exists(path)


def prepare_name_of_directory_measurements_for_n_cities(number_of_all_samples, number_of_cities):
    return "TSP_DIST_%d_N_%d" % (number_of_all_samples, number_of_cities)


def prepare_name_of_measurement_file_sample(number_of_sample, number_of_cities, format_of_file):
    return "TSP_CITIES_SET_%d_N_%d.%s" % (number_of_sample, number_of_cities, format_of_file)


def prepare_global_path_to_two_wrapped_directory(name_of_directory_1, name_of_directory_2):
    current_path = os.getcwd()
    return "%s/%s/%s" % (current_path, name_of_directory_1, name_of_directory_2)


def prepare_global_path_to_three_wrapped_directory(name_of_directory_1, name_of_directory_2, name_of_directory_3):
    current_path = os.getcwd()
    return "%s/%s/%s/%s" % (current_path, name_of_directory_1, name_of_directory_2, name_of_directory_3)


def prepare_global_path_to_wrapped_directory(name_of_directory_1):
    current_path = os.getcwd()
    return "%s/%s/" % (current_path, name_of_directory_1)


def prepare_directory_list_from_measurement_algorithm_name(name_of_algorithm, format_of_file):
    current_path = os.getcwd()
    path = "%s/%s/%s/%s" % (current_path, PATH_TO_MEASUREMENTS, format_of_file, name_of_algorithm)
    for _, dirs, _ in os.walk(path):
        return list(dirs).sort()


def prepare_files_list_from_measurement_algorithm_name_and_directory(name_of_algorithm, directory_wit_measurements_name,
                                                                     format_of_file):
    current_path = os.getcwd()
    path = "%s/%s/%s/%s/%s" % (
        current_path, PATH_TO_MEASUREMENTS, format_of_file, name_of_algorithm, directory_wit_measurements_name)
    for _, _, files in os.walk(path):
        return list(files).sort()


def prepare_path_to_save_csv_summary(name_of_algorithm, name_of_csv_summary_file):
    current_path = os.getcwd()
    return "%s/%s/feature/%s/%s" % (
        current_path, PATH_TO_MEASUREMENTS, name_of_algorithm, name_of_csv_summary_file)
