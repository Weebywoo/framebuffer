from dataclasses import dataclass, field

from framebuffer.math.linalg import Vector
import numpy


@dataclass
class Transform:
    position: Vector[numpy.float64] = field(default_factory=lambda: numpy.zeros(3, dtype=numpy.float64))
    scale: Vector[numpy.float64] = field(default_factory=lambda: numpy.ones(3, dtype=numpy.float64))
    rotation: Vector[numpy.float64] = field(
        default_factory=lambda: numpy.zeros(3, dtype=numpy.float64)
    )  # pitch, yaw, roll
