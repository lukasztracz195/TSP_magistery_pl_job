import time
import tracemalloc

from python_tsp.heuristics import solve_tsp_simulated_annealing

from algorithms.TSP import Tsp
from models.tsp_json_measurement import MeasurementForTime, MeasurementForTimeWithMalloc


class SimulatedAnnealingTsp(Tsp):
    def __init__(self, json_tsp):
        super().__init__(tsp_data_json=json_tsp)
        self.name = "simulated_annealing_heuristic_lib_python_tsp"

    def start_counting_with_time(self) -> MeasurementForTime:
        json_model = MeasurementForTime()

        start = time.clock()
        best_state, best_fitness = solve_tsp_simulated_annealing(self.cost_matrix)
        stop = time.clock()

        json_model.time_duration_in_sec = stop - start
        json_model.full_cost = best_fitness
        json_model.best_trace = self.move_solution_to_start_and_stop_from_the_same_node(best_state, 0)
        json_model.name_of_algorithm = self.name
        return json_model

    def start_counting_with_time_and_trace_malloc(self) -> MeasurementForTimeWithMalloc:
        json_model = MeasurementForTimeWithMalloc()
        self.clear_memory_before_measurement()

        tracemalloc.start()

        before_size, before_peak = tracemalloc.get_traced_memory()
        start = time.clock()

        best_state, best_fitness = solve_tsp_simulated_annealing(self.cost_matrix)

        stop = time.clock()
        after_size, after_peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        json_model.name_of_algorithm = self.name
        json_model.time_duration_in_sec = stop - start
        json_model.used_memory_before_measurement = before_size
        json_model.used_memory_peak_before_measurement = before_peak
        json_model.used_memory_diff_before_after_measurement = after_size - before_size
        json_model.used_memory_peak_diff_before_after_measurement = after_peak - before_peak
        json_model.used_memory_after_measurement = after_size
        json_model.used_memory_peak_after_measurement = after_peak
        json_model.full_cost = best_fitness
        json_model.best_trace = self.move_solution_to_start_and_stop_from_the_same_node(best_state, 0)
        return json_model
