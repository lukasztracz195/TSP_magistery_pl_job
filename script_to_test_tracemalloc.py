import sys
import tracemalloc
import gc


# bytes_on_float = 8
# expected_bytes = 10 * 10 * 10 * bytes_on_float
# expected_bytes = 8000
import numpy as np

gc.collect(generation=0)
gc.collect(generation=1)
gc.collect(generation=2)
tracemalloc.start()
tracemalloc.clear_traces()
before_current_size_memory_in_bytes, before_peak_of_size_memory_in_bytes = tracemalloc.get_traced_memory()
arr1 = np.ones([1024, 1, 1], dtype=np.int8)
after_current_size_memory_in_bytes, after_peak_of_size_memory_in_bytes = tracemalloc.get_traced_memory()
tracemalloc.stop()
diff_current_size_memory_in_bytes = after_current_size_memory_in_bytes - before_current_size_memory_in_bytes
diff_peak_of_size_memory_in_bytes = after_peak_of_size_memory_in_bytes - before_peak_of_size_memory_in_bytes
# print("sys.sizeof = ", sys.getsizeof(arr1))
# print("expected_allocated_memory:", expected_bytes)
print("size_of_memory_in_bytes_used_by_tracemalloc_module: ", tracemalloc.get_tracemalloc_memory())
print("before_current_size_memory_in_bytes: ", before_current_size_memory_in_bytes)
print("before_peak_of_size_memory_in_bytes", before_peak_of_size_memory_in_bytes)
print("after_current_size_memory_in_bytes", after_current_size_memory_in_bytes)
print("after_peak_of_size_memory_in_bytes", after_peak_of_size_memory_in_bytes)
print("diff_current_size_memory_in_bytes", diff_current_size_memory_in_bytes)
print("diff_peak_of_size_memory_in_bytes", diff_peak_of_size_memory_in_bytes)
