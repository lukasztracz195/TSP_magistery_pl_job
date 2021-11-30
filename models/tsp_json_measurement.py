class MeasurementForTime:

    def __init__(self):
        self.best_trace = None
        self.full_cost = None
        self.name_of_src_file = None
        self.time_duration_in_sec = None
        self.name_of_algorithm = None


class MeasurementForTimeWithMalloc:
    def __init__(self):
        self.best_trace = None
        self.full_cost = None
        self.name_of_src_file = None
        self.time_duration_in_sec = None
        self.used_memory_before_measurement = 0
        self.used_memory_peak_before_measurement = 0
        self.used_memory_diff_before_after_measurement = 0
        self.used_memory_peak_diff_before_after_measurement = 0
        self.used_memory_after_measurement = 0
        self.used_memory_peak_after_measurement = 0
        self.name_of_algorithm = None


class MeasurementForTimeForGenetic:

    def __init__(self):
        self.best_trace = None
        self.full_cost = None
        self.name_of_src_file = None
        self.time_duration_in_sec = None
        self.name_of_algorithm = None
        self.size_of_population = None
        self.probability_of_mutation = None
        self.max_attempts = None
        self.max_iterations = None
        self.random_state = None


class MeasurementForTimeWithMallocForGenetic:
    def __init__(self):
        self.best_trace = None
        self.full_cost = None
        self.name_of_src_file = None
        self.time_duration_in_sec = None
        self.used_memory_before_measurement = 0
        self.used_memory_peak_before_measurement = 0
        self.used_memory_diff_before_after_measurement = 0
        self.used_memory_peak_diff_before_after_measurement = 0
        self.used_memory_after_measurement = 0
        self.used_memory_peak_after_measurement = 0
        self.name_of_algorithm = None
        self.size_of_population = None
        self.probability_of_mutation = None
        self.max_attempts = None
        self.max_iterations = None
        self.random_state = None
