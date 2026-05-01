import time
from contextlib import contextmanager
from typing import Any, Generator


@contextmanager
def timer(time_keeper_list: list[float]) -> Generator[None, Any, None]:
    start_time: float = time.perf_counter_ns()

    yield

    end_time: float = time.perf_counter_ns()

    time_keeper_list.append(end_time - start_time)
