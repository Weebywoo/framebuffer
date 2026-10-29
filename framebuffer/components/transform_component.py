from typing import Literal, Optional

import numpy

from framebuffer.math.linalg import Vector
from framebuffer.scene.transform import Transform

from .base_component import BaseComponent


class TransformComponent(BaseComponent):
    def __init__(
        self,
        position: Optional[Vector[numpy.float64]] = None,
        scale: Optional[float] = None,
        rotation: Optional[Vector[numpy.float64]] = None,
    ) -> None:
        assert not all((position is None, scale is None, rotation is None))

        if position is not None:
            self.position: Vector[numpy.float64] = position

        else:
            self.position: Vector[numpy.float64] = numpy.zeros(3, dtype=numpy.float64)

        if scale is not None:
            self.scale: float = scale

        else:
            self.scale: float = 1.0

        if rotation is not None:
            self.rotation: Vector[numpy.float64] = rotation

        else:
            self.rotation: Vector[numpy.float64] = numpy.zeros(3, dtype=numpy.float64)

    def apply(self, transform: Transform, elapsed_time: float, dt: float) -> None:
        transform.position += self.position
        transform.rotation += self.rotation
        transform.scale *= self.scale
