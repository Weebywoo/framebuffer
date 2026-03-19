from dataclasses import dataclass, field

from ...linalg import Vector


@dataclass
class Vertex:
    position: Vector
    uv: Vector
    normal: Vector
    depth: float = field(default=float("inf"))
    inverted_w: float = field(default=0.0)
