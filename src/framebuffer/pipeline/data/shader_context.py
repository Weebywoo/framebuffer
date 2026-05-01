from dataclasses import dataclass

from ...linalg import Matrix
from ...rendering import Frame


@dataclass
class ShaderContext:
    model_matrix: Matrix
    view_matrix: Matrix
    projection_matrix: Matrix
    frame: Frame
    texture: list[list[list[int]]]
    texture_shape: tuple[int, int]
    clipping: tuple[float, float]
