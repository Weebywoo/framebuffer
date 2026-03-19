from __future__ import annotations

from typing import Iterable, Literal

from .vector import Vector


class Matrix:
    def __init__(self, /, matrix: Iterable[Iterable[float]]) -> None:
        self._matrix: list[list[float]] = list(list(row) for row in matrix)
        self._shape: tuple[int, int] = (len(self._matrix), len(self._matrix[0]))

    @classmethod
    def zeros(cls, shape: tuple[int, int]) -> Matrix:
        return cls([[0.0 for _ in range(shape[0])] for _ in range(shape[1])])

    @property
    def shape(self) -> tuple[int, int]:
        return self._shape

    def take(self, index: int, /, axis: Literal[0, 1] = 0) -> Vector:
        match axis:
            case 0:
                return Vector(self._matrix[index])

            case 1:
                return Vector(row[index] for row in self._matrix)

            case _:
                raise NotImplementedError

    def __setitem__(self, key: tuple[int, int], value: float, /) -> None:
        y, x = key
        self._matrix[y][x] = value

    def __matmul__[OtherType](self, other: OtherType, /) -> OtherType:
        rows_self: list[Vector] = [self.take(index, axis=0) for index in range(self._shape[0])]

        if isinstance(other, Matrix):
            columns_other: list[Vector] = [other.take(index, axis=1) for index in range(other.shape[0])]

            return Matrix([[row.dot(column) for column in columns_other] for row in rows_self])

        elif isinstance(other, Vector):
            return Vector([row.dot(other) for row in rows_self])

        else:
            raise NotImplementedError
