# https://github.com/LucienShui/timer

import time
from contextlib import contextmanager


@contextmanager
def timer(name):
    """
    context manager for profiling python code execution time
    """
    start = time.perf_counter()
    yield 
    print(name, time.perf_counter() - start)

