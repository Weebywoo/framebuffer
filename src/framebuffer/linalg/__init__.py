from .matrix3x3 import Matrix3x3
from .matrix4x4 import Matrix4x4
from .vector2 import Vector2
from .vector3 import Vector3
from .vector4 import Vector4

__all__ = [
    "lerp4d",
    "Vector2",
    "Vector4",
    "Vector3",
    "Matrix3x3",
    "Matrix4x4",
]


def lerp4d(a: Vector4, b: Vector4, t: float) -> Vector4:
    return a * t + b * (1 - t)
