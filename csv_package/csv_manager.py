import csv
from csv import DictWriter
from csv_package.csv_record import CsvRecord
from functions import exist_file


class CsvManager:

    def __init__(self, path_to_csv):
        self.__path_to_csv = path_to_csv
        self.__appended_rows = 0



    def append_row_to_file(self, csv_record_obj: CsvRecord):
        if not exist_file(self.__path_to_csv):
            self.__create_csv_file(csv_record_obj)

        with open(self.__path_to_csv, 'a', encoding='UTF8', newline="") as f_object:
            dict_writer_object = DictWriter(f_object, fieldnames=csv_record_obj.column_names)
            dict_writer_object.writerow(csv_record_obj.record_dict)
            self.__appended_rows += 1
            f_object.close()

    def __create_csv_file(self, csv_record_obj: CsvRecord):
        with open(self.__path_to_csv, 'w', encoding='UTF8', newline="") as f:
            writer = csv.writer(f)
            writer.writerow(csv_record_obj.column_names)

    @property
    def appended_rows(self):
        return self.__appended_rows
