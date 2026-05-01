from .linalg import Vector, Matrix

__all__ = [
    "lerp",
    "get_lerp_fraction",
    "Vector",
    "Matrix",
]


def lerp[Type](a: Type, b: Type, t: float) -> Type:
    return a * t + b * (1 - t)


def get_lerp_fraction[Type](vertex_A: Type, vertex_B: Type, clipping: float) -> float:
    return (clipping - vertex_A.position.z) / (vertex_B.position.z - vertex_A.position.z)
