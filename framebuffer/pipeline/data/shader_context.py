from dataclasses import dataclass
from typing import TYPE_CHECKING

import numpy

from framebuffer.math.linalg import Matrix, MatrixNDIM, Vector

if TYPE_CHECKING:
    from framebuffer.rendering.frame import Frame


@dataclass
class ShaderContext:
    model_matrix: Matrix[numpy.float64]
    view_matrix: Matrix[numpy.float64]
    projection_matrix: Matrix[numpy.float64]
    frame: Frame
    texture: MatrixNDIM[numpy.uint8]
    clipping: Vector[numpy.float64]
