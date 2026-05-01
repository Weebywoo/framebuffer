from dataclasses import dataclass, field

from ...linalg import Vector


@dataclass
class Vertex:
    position: Vector
    uv: Vector
    normal: Vector
    depth: float = field(default=float("inf"))
    inverted_w: float = field(default=0.0)

    def __repr__(self) -> str:
        return "Vertex(position={0}, uv={1}, normal={2}, depth={3}, inverted_w={4})".format(
            self.position, self.uv, self.normal, self.depth, self.inverted_w
        )
