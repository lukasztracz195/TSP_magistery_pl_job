import threading
import time
import pandas as pd
import psutil

from collector.DataCollector import DataCollector
from constants.CsvColumnNames import *

DEFAULT_VALUE = "TOO_SHORT_TIME_EXEC_TO_PROFILE_CPU_AND_RAM"


class CpuProfiler(threading.Thread):
    def __init__(self):
        super().__init__()
        self.interval_in_seconds = 1
        self.collector = DataCollector()
        self.stopped = False
        self.after = time.perf_counter()
        self.collector.add_data(UTILIZATION_OF_CPU, list())
        self.start_time = None

    def run(self):
        initialized = False
        self.start_time = time.clock()
        while not self.stopped:
            if not initialized:
                self.make_measure()
                initialized = True
                self.after = time.perf_counter() + self.interval_in_seconds
            else:
                if time.perf_counter() > self.after:
                    self.make_measure()
                    self.after = time.perf_counter() + self.interval_in_seconds
            if self.stopped:
                break

    def make_measure(self):
        if not self.stopped:
            self.collector.add_data_to_list(UTILIZATION_OF_CPU, psutil.cpu_percent(0.1))

    def stop(self):
        self.stopped = True
        stop = time.clock()
        self.collector.add_data(TIME_DURATION_IN_SEC,
                                stop - self.start_time)

    def get_collector(self):
        fields = [UTILIZATION_OF_CPU]
        for field in fields:
            if len(self.collector.dictionary_of_data[field]) == 0:
                self.collector.dictionary_of_data[field] = DEFAULT_VALUE
        series = pd.Series(self.collector.dictionary_of_data[UTILIZATION_OF_CPU])
        self.collector.dictionary_of_data[MIN_UTILIZATION_OF_CPU] = series.min()
        self.collector.dictionary_of_data[AVG_UTILIZATION_OF_CPU] = series.mean()
        self.collector.dictionary_of_data[MAX_UTILIZATION_OF_CPU] = series.max()
        self.collector.dictionary_of_data[STD_UTILIZATION_OF_CPU] = series.std()
        return self.collector
