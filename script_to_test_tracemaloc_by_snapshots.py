import gc
import tracemalloc
import sys
import numpy as np

# bytes_on_float = 8
# expected_bytes = 10 * 10 * 10 * bytes_on_float
# expected_bytes = 8000
gc.collect(generation=0)
gc.collect(generation=1)
gc.collect(generation=2)
tracemalloc.start()
tracemalloc.clear_traces()
before_snapshot = tracemalloc.take_snapshot()
arr1 = np.ones([1024, 1, 1], dtype=np.int8)
after_snapshot = tracemalloc.take_snapshot()
tracemalloc.stop()
diff_snapshot = after_snapshot.compare_to(before_snapshot, 'lineno')
print("<DIFF SNAPSOTS>")
# for diff in diff_snapshot:
#     #if "tracemalloc_ex6.py" in str(diff):
#     print(diff)
# print("</DIFF SNAPSOTS>")
allocated_memory_list = list(filter(lambda x: x.count_diff == 0 or x.size_diff == 0, diff_snapshot))
# for diff in allocated_memory_list:
#     print(diff)
allocated_memory = sum(map(lambda x: x.size, allocated_memory_list))
print("allocated_memory: ", allocated_memory)
print("sys.sizeof = ", sys.getsizeof(arr1))
# print("expected_allocated_memory:", expected_bytes)
print("size_of_memory_in_bytes_used_by_tracemalloc_module: ", tracemalloc.get_tracemalloc_memory())
