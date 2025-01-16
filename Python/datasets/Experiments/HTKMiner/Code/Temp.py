import os

import timeit
from itertools import islice

# Large dictionary
my_dict = {i: f"value_{i}" for i in range(1_000_000)}

# Using islice
def use_islice():
    return dict(islice(my_dict.items(), 10))

# Using list slicing
def use_list_slicing():
    return dict(list(my_dict.items())[:10])

# Measure time
islice_time = timeit.timeit(use_islice, number=1000)
slicing_time = timeit.timeit(use_list_slicing, number=1000)

print(f"islice: {islice_time:.6f} seconds")
print(f"list slicing: {slicing_time:.6f} seconds")