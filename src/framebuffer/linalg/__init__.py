from .vector import Vector
from .matrix import Matrix

__all__ = [
    "lerp",
    "Vector",
    "Matrix",
]


def lerp(a: Vector, b: Vector, t: float) -> Vector:
    return a * t + b * (1 - t)
