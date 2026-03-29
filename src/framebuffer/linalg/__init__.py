from .linalg import Vector, Matrix

__all__ = [
    "lerp",
    "Vector",
    "Matrix",
]


def lerp(a: Vector, b: Vector, t: float) -> Vector:
    return a * t + b * (1 - t)
