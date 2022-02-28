from builders.PathBuilder import PathBuilder
import pandas as pd
from constants.CsvColumnNames import *

SUFFIX = "suffix "
TYPE_OF_MEASUREMENTS = ["CPU", "TIME_AND_DATA", "TIME_AND_MEMORY"]
TYPE_MEASUREMENT = "TIME_AND_MEMORY"
PATH_TO_SRC_CSV = PathBuilder() \
    .add_dir("measurements") \
    .add_dir("local_search_compare_any_pertrubation_modes") \
    .add_file_with_extension("%s.csv" % TYPE_MEASUREMENT) \
    .build()

df = pd.read_csv(PATH_TO_SRC_CSV)
print("columns: ", df.columns)
# suffix_panda_dictionary = dict()
all_suffix = list(df[SUFFIX].unique())
for suffix in all_suffix:
    tmp_df = df[df[SUFFIX] == suffix]
    tmp_df.reset_index(drop=True, inplace=True)
    path_to_output_csv = PathBuilder() \
        .add_dir("measurements") \
        .add_dir("local_search_compare_any_pertrubation_modes") \
        .add_file_with_extension("%s_%s.csv" % (TYPE_MEASUREMENT, suffix.strip())) \
        .build()
    tmp_df.to_csv(path_to_output_csv)
