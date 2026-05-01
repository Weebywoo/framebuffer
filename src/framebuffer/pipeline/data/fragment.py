from dataclasses import dataclass

from ...linalg import Vector


@dataclass
class Fragment:
    position: Vector
    depth: float
    uv: Vector
