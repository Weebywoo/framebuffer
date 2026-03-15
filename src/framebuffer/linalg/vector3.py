from __future__ import annotations

from typing import Generator, Any

from .vector2 import Vector2


class Vector3:
    def __init__(self, x: float, y: float, z: float) -> None:
        self.x: float = x
        self.y: float = y
        self.z: float = z

    def to_2d(self) -> Vector2:
        return Vector2(x=self.x, y=self.y)

    @property
    def magnitude(self) -> float:
        return sum(self_value**2 for self_value in self) ** 0.5

    @property
    def normalised(self) -> Vector3:
        return Vector3(x=self.x, y=self.y, z=self.z) / self.magnitude

    @staticmethod
    def zeros() -> Vector3:
        return Vector3(x=0.0, y=0.0, z=0.0)

    @staticmethod
    def ones() -> Vector3:
        return Vector3(x=1.0, y=1.0, z=1.0)

    def __sub__(self, other: Vector3) -> Vector3:
        return Vector3(x=self.x - other.x, y=self.y - other.y, z=self.z - other.z)

    def __add__(self, other: Vector3) -> Vector3:
        return Vector3(x=self.x + other.x, y=self.y + other.y, z=self.z + other.z)

    def dot(self, other: Vector3) -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def __iadd__(self, other: Vector3) -> Vector3:
        self.x += other.x
        self.y += other.y
        self.z += other.z

        return self

    def cross(self, other: Vector3) -> Vector3:
        return Vector3(
            x=(self.y * other.z) - (self.z * other.y),
            y=(self.z * other.x) - (self.x * other.z),
            z=(self.x * other.y) - (self.y * other.x),
        )

    def __mul__(self, scalar: float) -> Vector3:
        return Vector3(x=self.x * scalar, y=self.y * scalar, z=self.z * scalar)

    def __truediv__(self, scalar: float) -> Vector3:
        return Vector3(x=self.x / scalar, y=self.y / scalar, z=self.z / scalar)

    def __iter__(self) -> Generator[float, Any, None]:
        for value in [self.x, self.y, self.z]:
            yield value
