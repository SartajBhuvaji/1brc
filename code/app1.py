import time
from typing import Dict, Callable
from functools import wraps
import mmap

def timer_decorator(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} executed in {end_time - start_time:.4f} seconds")
        return result
    return wrapper


@timer_decorator
def calculate_stats(file):
    stats: Dict[str, List[float]] = {}
  
    with open(file, "rb") as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        for line in iter(mm.readline, b''):
            city, temp_str = line.decode('utf-8').strip().split(';')
            temp = float(temp_str)
            if city in stats:
                stats[city][0] += 1
                stats[city][1] += temp
                stats[city][2] = min(stats[city][2], temp)
                stats[city][3] = max(stats[city][3], temp)
            else:
                stats[city] = [1, temp, temp, temp]

    return stats

@timer_decorator
def print_stats(stats):
    formatted = ', '.join(
        f"{k} = {v[2]}/ {v[1]/v[0]:.2f}/ {v[3]}"
        for k, v in sorted(stats.items())
    )
    print("{" + formatted + "}")

stats = calculate_stats("../data/short.txt")
print_stats(stats)