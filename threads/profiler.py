import threading
import time

import psutil

from collector.DataCollector import DataCollector
from constants import MeasurementCpuProfiler


class CpuProfiler(threading.Thread):
    def __init__(self):
        super().__init__()
        self.interval_in_seconds = 5
        self.collector = DataCollector()
        self.stopped = False
        self.after = time.perf_counter()
        self.collector.add_data(MeasurementCpuProfiler.USED_READ_ACCESS_MEMORY_IN_BYTES, list())
        self.collector.add_data(MeasurementCpuProfiler.UTILIZATION_OF_CPU, list())
        self.collector.add_data(MeasurementCpuProfiler.USED_READ_ACCESS_MEMORY_IN_PERCENTAGE, list())
        self.collector.add_data(MeasurementCpuProfiler.CPU_FREQUENCY_IN_MHZ, list())

    def run(self):
        initialized = False
        while not self.stopped:
            if not initialized:
                self.make_measure()
                initialized = True
                self.after = time.perf_counter() + self.interval_in_seconds
            else:
                if time.perf_counter() > self.after:
                    self.make_measure()
                    self.after = time.perf_counter() + self.interval_in_seconds

    def make_measure(self):
        if not self.stopped:
            self.collector.add_data_to_list(MeasurementCpuProfiler.USED_READ_ACCESS_MEMORY_IN_BYTES,
                                            int(psutil.virtual_memory().total - psutil.virtual_memory().available))
            self.collector.add_data_to_list(MeasurementCpuProfiler.UTILIZATION_OF_CPU, psutil.cpu_percent(interval=0.5))
            self.collector.add_data_to_list(MeasurementCpuProfiler.USED_READ_ACCESS_MEMORY_IN_PERCENTAGE,
                                            psutil.virtual_memory().percent)
            self.collector.add_data_to_list(MeasurementCpuProfiler.CPU_FREQUENCY_IN_MHZ, int(psutil.cpu_freq().current))

    def stop(self):
        self.stopped = True

    def get_collector(self):
        return self.collector
