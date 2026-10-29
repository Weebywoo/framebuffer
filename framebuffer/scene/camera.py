import math
from dataclasses import dataclass, field

import numpy

from framebuffer.math.linalg import Vector
from framebuffer.scene.entity import Entity

DEFAULT_FOW: float = math.radians(60)


@dataclass(kw_only=True)
class Camera(Entity):
    fov: float = field(default=DEFAULT_FOW)
    clipping: Vector[numpy.float64]
