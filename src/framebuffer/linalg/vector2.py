from __future__ import annotations


class Vector2:
    def __init__(self, x: float, y: float) -> None:
        self.x: float = x
        self.y: float = y

    def __truediv__(self, scalar: float) -> Vector2:
        return Vector2(x=self.x / scalar, y=self.y / scalar)

    def __add__(self, other: Vector2) -> Vector2:
        return Vector2(x=self.x + other.x, y=self.y + other.y)

    def __sub__(self, other: Vector2) -> Vector2:
        return Vector2(x=self.x - other.x, y=self.y - other.y)

    def __mul__(self, scalar: float) -> Vector2:
        return Vector2(x=self.x * scalar, y=self.y * scalar)

    def dot(self, other: Vector2) -> float:
        return self.x * other.x + self.y * other.y
