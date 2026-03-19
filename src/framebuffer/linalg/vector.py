from __future__ import annotations

from typing import Iterable, Any, Generator


class Vector:
    def __init__(self, /, values: Iterable[Any]) -> None:
        self._values: tuple[float, ...] = tuple(values)

    @classmethod
    def zeros(cls, length: int) -> Vector:
        return cls([0.0] * length)

    @classmethod
    def fill(cls, value: Any, /, length: int) -> Vector:
        return cls([value] * length)

    @property
    def x(self) -> float:
        return self._values[0]

    @property
    def y(self) -> float:
        return self._values[1]

    @property
    def z(self) -> float:
        return self._values[2]

    @property
    def w(self) -> float:
        return self._values[3]

    @property
    def magnitude(self) -> float:
        return sum(value**2 for value in self) ** 0.5

    @property
    def normalised(self) -> Vector:
        return self / self.magnitude

    def dot(self, other: Vector) -> float:
        return sum(value * other_value for value, other_value in zip(self, other))

    def cross(self, other: Vector) -> Vector:
        return Vector(
            [
                self.y * other.z - self.z * other.y,
                self.z * other.x - self.x * other.z,
                self.x * other.y - self.y * other.x,
            ]
        )

    def astype(self, dtype: type, /) -> Vector:
        return Vector(map(dtype, self))

    def __getitem__(self, index: int) -> float:
        return self._values[index]

    def __len__(self) -> int:
        return len(self._values)

    def __iter__(self) -> Generator[float, Any, None]:
        for value in self._values:
            yield value

    def __neg__(self) -> Vector:
        def func(value: float) -> float:
            return -value

        return Vector(map(func, self))

    def __truediv__(self, other_value: float | int) -> Vector:
        def func(value: float) -> float:
            return value / other_value

        return Vector(map(func, self))

    def __floordiv__(self, other_value: float | int) -> Vector:
        def func(value: float) -> float:
            return value // other_value

        return Vector(map(func, self))

    def __mul__(self, other_value: float | int) -> Vector:
        def func(value: float) -> float:
            return value * other_value

        return Vector(map(func, self))

    def __add__(self, other: Vector) -> Vector:
        def func(value: float, other_value: float) -> float:
            return value + other_value

        return Vector(map(func, self, other))

    def __iadd__(self, other: Vector) -> Vector:
        def func(value: float, other_value: float) -> float:
            return value + other_value

        self._values = tuple(map(func, self, other))

        return self

    def __sub__(self, other: Vector) -> Vector:
        def func(value: float, other_value: float) -> float:
            return value - other_value

        return Vector(map(func, self, other))
