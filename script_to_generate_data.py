import json
import os

import pandas as pd

from constants.InputCityDataJson import *
from data_generator.CityGenerator import CityGenerator
from functions import exist_file
from models.City import City
from progress.progress import progress_bar

PATH_TO_DATASET = "./dataset/"

NUMBER_OF_SETS = 100

DISTANCE = 1000
MIN_X = -DISTANCE
MAX_X = DISTANCE
MIN_Y = -DISTANCE
MAX_Y = DISTANCE

# N_SETS = [3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]
N_SETS = list(range(3, 51))


def prepare_stats(generated_city):
    stats = {X: dict(), Y: dict()}
    xs = [city.x for city in generated_city]
    ys = [city.y for city in generated_city]
    xs_series = pd.Series(xs).sort_values()
    ys_series = pd.Series(ys).sort_values()
    xs_mean = xs_series.mean()
    ys_mean = ys_series.mean()
    xs_std = xs_series.std()
    ys_std = ys_series.std()
    xs_median = xs_series.median()
    ys_median = ys_series.median()
    xs_q1 = xs_series.quantile(.25)
    ys_q1 = ys_series.quantile(.25)
    xs_q3 = xs_series.quantile(.75)
    ys_q3 = ys_series.quantile(.75)
    stats[X][MIN] = xs_series.min()
    stats[Y][MIN] = ys_series.min()
    stats[X][AVG] = xs_mean
    stats[Y][AVG] = ys_mean
    stats[X][STDEV] = xs_std
    stats[Y][STDEV] = ys_std
    stats[X][MEDIAN] = xs_median
    stats[Y][MEDIAN] = ys_median
    stats[X][Q1] = xs_q1
    stats[Y][Q1] = ys_q1
    stats[X][Q3] = xs_q3
    stats[Y][Q3] = ys_q3
    stats[X][MAX] = xs_series.max()
    stats[Y][MAX] = ys_series.max()
    return stats


def prepare_distance_matrix(generated_city):
    distance_matrix = dict()
    for out_city in generated_city:
        for in_city in generated_city:
            distance_matrix[out_city.number_of_city] = {in_city.number_of_city: City.count_distance(out_city, in_city)}
    return distance_matrix


START_CITY = City(number_of_city=0, x=0, y=0)
generator = CityGenerator(min_x=MIN_X, max_x=MAX_X, min_y=MIN_Y, max_y=MAX_Y, start_city=START_CITY)

total = pd.Series(N_SETS).multiply(NUMBER_OF_SETS).sum()
current = 0
for NUMBER_OF_CITIES_IN_SET in N_SETS:
    NAME_OF_DIRECTORY = "TSP_DIST_%d_N_%d" % (DISTANCE, NUMBER_OF_CITIES_IN_SET)
    for number_of_set in range(11, NUMBER_OF_SETS):
        JSON_DICT = dict()
        JSON_DICT[CITIES] = []
        JSON_DICT[DISTANCE_MATRIX] = dict()
        JSON_DICT[STATS] = {X: dict(), Y: dict()}
        generated_cities = generator.generate_cities(NUMBER_OF_CITIES_IN_SET, distinct=True)
        generated_cities_by_number_city_order = sorted(generated_cities, key=lambda x: x.number_of_city)
        for generated_city in generated_cities_by_number_city_order:
            JSON_DICT[CITIES].append({
                NUMBER_OF_CITY: generated_city.number_of_city,
                X: generated_city.x,
                Y: generated_city.y})
        stats = prepare_stats(generated_cities_by_number_city_order)
        JSON_DICT[STATS] = stats
        distance_matrix = prepare_distance_matrix(generated_cities_by_number_city_order)
        JSON_DICT[DISTANCE_MATRIX] = distance_matrix
        json_as_str = json.dumps(JSON_DICT)
        json_name_of_file = "TSP_CITIES_SET_%d_N_%d.json" % (number_of_set, NUMBER_OF_CITIES_IN_SET)
        if not os.path.exists(PATH_TO_DATASET + NAME_OF_DIRECTORY):
            os.mkdir(PATH_TO_DATASET + NAME_OF_DIRECTORY)
        path_to_json_file = PATH_TO_DATASET + NAME_OF_DIRECTORY + "/" + json_name_of_file
        if not exist_file(path_to_json_file):
            jsons_file = open(path_to_json_file, "w")
            jsons_file.write(json_as_str)
            jsons_file.close()
        current += 1
        progress_bar(current, total, "generate_data")
