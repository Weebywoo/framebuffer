from __future__ import annotations

from typing import Iterable, Any, Generator, Literal


class Vector:
    def __init__(self, values: Iterable[Any], /) -> None:
        self._values: list[float] = list(values)

    @classmethod
    def zero(cls, length: int) -> Vector:
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

    def dot(self, other: Vector, /) -> float:
        return sum(value * other_value for value, other_value in zip(self, other))

    def cross(self, other: Vector, /) -> Vector:
        return Vector(
            [
                self.y * other.z - self.z * other.y,
                self.z * other.x - self.x * other.z,
                self.x * other.y - self.y * other.x,
            ]
        )

    def astype(self, dtype: type, /) -> Vector:
        return Vector(map(dtype, self))

    def __len__(self) -> int:
        return len(self._values)

    def __getitem__(self, index: int, /) -> float:
        return self._values[index]

    def __iter__(self) -> Generator[float, Any, None]:
        for value in self._values:
            yield value

    def __neg__(self) -> Vector:
        def func(value: float) -> float:
            return -value

        return Vector(map(func, self))

    def __truediv__(self, other_value: float | int, /) -> Vector:
        def func(value: float) -> float:
            return value / other_value

        return Vector(map(func, self))

    def __floordiv__(self, other_value: float | int, /) -> Vector:
        def func(value: float) -> float:
            return value // other_value

        return Vector(map(func, self))

    def __mul__(self, other_value: float | int, /) -> Vector:
        def func(value: float) -> float:
            return value * other_value

        return Vector(map(func, self))

    def __add__(self, other: Vector, /) -> Vector:
        def func(value: float, other_value: float) -> float:
            return value + other_value

        return Vector(map(func, self, other))

    def __iadd__(self, other: Vector, /) -> Vector:
        def func(value: float, other_value: float) -> float:
            return value + other_value

        self._values = list(map(func, self, other))

        return self

    def __sub__(self, other: Vector, /) -> Vector:
        def func(value: float, other_value: float) -> float:
            return value - other_value

        return Vector(map(func, self, other))

    def __matmul__(self, other: Matrix, /) -> Vector:
        if not isinstance(other, Matrix):
            raise TypeError(f"Unsupported operand type(s) for @: 'Vector' and '{type(other).__name__}'")

        columns_other: list[Vector] = [other.take(column_index, axis=1) for column_index in range(other.shape[1])]

        return Vector(map(self.dot, columns_other))


class Matrix:
    def __init__(self, matrix: Iterable[Iterable[float]], /, shape: tuple[int, int]) -> None:
        self._values: list[list[float]] = list(list(row) for row in matrix)
        self._shape: tuple[int, int] = shape

    @property
    def transpose(self) -> Matrix:
        return Matrix(
            [[self._values[y][x] for y in range(self._shape[0])] for x in range(self._shape[1])], shape=self.shape
        )

    @classmethod
    def zeros(cls, shape: tuple[int, int]) -> Matrix:
        return cls([[0.0 for _ in range(shape[1])] for _ in range(shape[0])], shape=shape)

    @property
    def shape(self) -> tuple[int, int]:
        return self._shape

    def take(self, index: int, /, axis: Literal[0, 1] = 0) -> Vector:
        match axis:
            case 0:
                return Vector(self._values[index])

            case 1:
                return Vector(row[index] for row in self._values)

            case _:
                raise IndexError("Invalid axis")

    def __setitem__(self, key: tuple[int, int], value: float, /) -> None:
        y, x = key
        self._values[y][x] = value

    def __getitem__(self, key: tuple[int, int], /) -> float:
        y, x = key

        return self._values[y][x]

    def __matmul__(self, other: Matrix, /) -> Matrix:
        if not isinstance(other, Matrix):
            raise TypeError(f"Unsupported operand type(s) for @: 'Matrix' and '{type(other).__name__}'")

        rows_self: list[Vector] = [self.take(row_index, axis=0) for row_index in range(self._shape[1])]
        columns_other: list[Vector] = [other.take(column_index, axis=1) for column_index in range(other.shape[0])]

        return Matrix(
            [[row.dot(column) for column in columns_other] for row in rows_self],
            shape=(other.shape[1], self._shape[0]),
        )
