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
        scale_mode: Literal["add", "multiply"] = "add",
    ) -> None:
        assert not all((position is None, scale is None, rotation is None))

        self.position: Vector[numpy.float64] = position or numpy.zeros(3, dtype=numpy.float64)
        self.scale: float = scale or 1.0
        self.rotation: Vector[numpy.float64] = rotation or numpy.zeros(3, dtype=numpy.float64)
        self.scale_mode: Literal["add", "multiply"] = scale_mode

    def apply(self, transform: Transform, elapsed_time: float, dt: float) -> None:
        transform.position += self.position
        transform.rotation += self.rotation

        match self.scale_mode:
            case "add":
                transform.scale += self.scale

            case "multiply":
                transform.scale *= self.scale
