from dataclasses import dataclass, field

import numpy

from framebuffer.math.linalg import Vector


@dataclass
class Vertex:
    position: Vector[numpy.float64]  # 4 -> 0:4
    uv: Vector[numpy.float64]  # 2 -> 4:6
    normal: Vector[numpy.float64]  # 3 -> 6:9
    depth: numpy.float64 = field(default=numpy.inf)  # 1 -> 9
    inverted_w: numpy.float64 = field(default_factory=numpy.float64)  # 1 -> 10
