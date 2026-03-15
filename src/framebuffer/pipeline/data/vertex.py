from dataclasses import dataclass, field

from ...linalg import Vector2, Vector3, Vector4


@dataclass
class Vertex:
    position: Vector4
    uv: Vector2
    normal: Vector3
    depth: float = field(default=float("inf"))
    inverted_w: float = field(default=0.0)
