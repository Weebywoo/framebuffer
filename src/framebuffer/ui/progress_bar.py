import datetime
import time
from datetime import timedelta
from typing import Iterable, Any, Generator, Optional


class ProgressBar[Type]:
    def __init__(self, iterable: Iterable[Type], name: Optional[str] = None) -> None:
        self.iterable: Iterable[Type] = iterable
        self.length: int = len(list(iterable))
        self.bar_length: int = 35
        self.timestamp_last_iteration: float | None = None
        self.name: str = f" {name}" if name else "it"

    def _generate_bar(self, percent: float) -> str:
        bar: str = "█" * int(self.bar_length * percent)

        if len(bar) == self.bar_length:
            return bar

        rest: float = self.bar_length * percent - len(bar)

        if rest <= 1 / 8:
            bar += "▏"

        elif rest <= 2 / 8:
            bar += "▎"

        elif rest <= 3 / 8:
            bar += "▍"

        elif rest <= 4 / 8:
            bar += "▌"

        elif rest <= 5 / 8:
            bar += "▋"

        elif rest <= 6 / 8:
            bar += "▊"

        elif rest <= 7 / 8:
            bar += "▉"

        elif rest <= 8 / 8:
            bar += "█"

        return bar

    def __iter__(self) -> Generator[Type, Any, None]:
        start_time: datetime.datetime = datetime.datetime.now()
        iteration_times: list[float] = []

        for index, value in enumerate(self.iterable, 1):
            last_iteration_duration: float = 0.0

            if self.timestamp_last_iteration is not None:
                last_iteration_duration = time.time() - self.timestamp_last_iteration

            self.timestamp_last_iteration = time.time()

            iteration_times.append(last_iteration_duration)

            percent: float = index / self.length
            bar = self._generate_bar(percent)
            fraction: str = f"{str(index).rjust(len(str(self.length)))} / {self.length}"
            elapsed_time: timedelta = datetime.datetime.now() - start_time
            average_it_duration: float = sum(iteration_times) / len(iteration_times)
            it_per_second: float = 0.0

            if average_it_duration > 0.0:
                it_per_second = round(1 / average_it_duration, 2)

            predicted_total_time: timedelta = timedelta(seconds=0.0)

            if it_per_second > 0.0:
                predicted_total_time = timedelta(seconds=self.length / it_per_second)

            time_left: timedelta = timedelta(seconds=0)

            if index != self.length:
                time_left = predicted_total_time - elapsed_time

            print(
                "\033[1;1H{percent}% | {bar} | {fraction} [{elapsed_time}<{time_left}<{predicted_total_time}, {average_it_duration}, {it_per_second}{name}/s]".format(
                    percent=f"{round(percent * 100, 2):.2f}".rjust(6),
                    bar=bar.ljust(self.bar_length),
                    fraction=fraction,
                    elapsed_time=str(elapsed_time)[:7],
                    time_left=str(time_left)[:7],
                    predicted_total_time=str(predicted_total_time)[:7],
                    average_it_duration=f"{average_it_duration:.2f}s",
                    it_per_second=f"{it_per_second:.2f}",
                    name=self.name,
                )
            )

            yield value
