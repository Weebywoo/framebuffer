from __future__ import annotations

from typing import Generator, Any


class Vector4:
    def __init__(self, x: float, y: float, z: float, w: float) -> None:
        self.x: float = x
        self.y: float = y
        self.z: float = z
        self.w: float = w

    @staticmethod
    def zeros(dtype: type = float) -> Vector4:
        return Vector4(*[dtype()] * 4)

    def dot(self, other: Vector4) -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z + self.w * other.w

    def __sub__(self, other: Vector4) -> Vector4:
        return Vector4(
            x=self.x - other.x,
            y=self.y - other.y,
            z=self.z - other.z,
            w=self.w - other.w,
        )

    def __add__(self, other: Vector4) -> Vector4:
        return Vector4(
            x=self.x + other.x,
            y=self.y + other.y,
            z=self.z + other.z,
            w=self.w + other.w,
        )

    def __iadd__(self, other: Vector4) -> Vector4:
        self.x += other.x
        self.y += other.y
        self.z += other.z
        self.w += other.w

        return self

    def __mul__(self, scalar: float) -> Vector4:
        return Vector4(x=self.x * scalar, y=self.y * scalar, z=self.z * scalar, w=self.w * scalar)

    def __truediv__(self, scalar: float) -> Vector4:
        return Vector4(x=self.x / scalar, y=self.y / scalar, z=self.z / scalar, w=self.w / scalar)

    def __neg__(self) -> Vector4:
        return Vector4(x=-self.x, y=-self.y, z=-self.z, w=-self.w)

    def __iter__(self) -> Generator[float, Any, None]:
        for value in [self.x, self.y, self.z, self.w]:
            yield value
