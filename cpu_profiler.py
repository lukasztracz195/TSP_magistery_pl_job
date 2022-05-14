import psutil
import os

from builders.PathBuilder import PathBuilder
from constants.CsvColumnNames import UTILIZATION_OF_CPU
from csv_package.csv_manager import CsvManager
from csv_package.csv_record import CsvRecord
from collector.DataCollector import DataCollector

PROFILER_IN_PROGRESS = "PROFILER_IN_PROGRESS.txt"
MEASURE_IN_PROGRESS = "MEASURE_IN_PROGRESS.txt"

path_to_profiler_file = PathBuilder().add_dir("tmp").add_file_with_extension(PROFILER_IN_PROGRESS).build()
path_to_measure_file = PathBuilder().add_dir("tmp").add_file_with_extension(MEASURE_IN_PROGRESS).build()


def read_pid_from_pidfile(pidfile_path):
    """ Read the PID recorded in the named PID file.

        Read and return the numeric PID recorded as text in the named
        PID file. If the PID file cannot be read, or if the content is
        not a valid PID, return ``None``.

        """
    pid = None
    try:
        pidfile = open(pidfile_path, 'r')
    except IOError:
        pass
    else:
        # According to the FHS 2.3 section on PID files in /var/run:
        #
        #   The file must consist of the process identifier in
        #   ASCII-encoded decimal, followed by a newline character.
        #
        #   Programs that read PID files should be somewhat flexible
        #   in what they accept; i.e., they should ignore extra
        #   whitespace, leading zeroes, absence of the trailing
        #   newline, or additional lines in the PID file.

        line = pidfile.readline().strip()
        try:
            pid = int(line)
        except ValueError:
            pass
        pidfile.close()

    return pid


def save_file(path):
    f = open(path, "a")
    f.write("")
    f.close()


def delete_file(path):
    if os.path.exists(path):
        os.remove(path)


def file_exist(path):
    return os.path.exists(path)


def main():
    collector = DataCollector()
    p = psutil.Process(os.getpid())
    p.nice(psutil.HIGH_PRIORITY_CLASS)
    save_file(path_to_profiler_file)
    csv_manager = CsvManager(path_to_csv=path_to_output_csv)
    csv_record = CsvRecord()
    while True:
        if file_exist(path_to_measure_file):
            PID = read_pid_from_pidfile(path_to_measure_file)
            p = psutil.Process(PID)
            while file_exist(path_to_measure_file):
                collector.add_data(UTILIZATION_OF_CPU, p.cpu_percent() / psutil.cpu_count())
            csv_record.set_values_from_dict(collector.get_dictionary_with_data())
            csv_manager.append_row_to_file(csv_record)
            break
    delete_file(path_to_profiler_file)
main()
