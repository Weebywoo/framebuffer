from dataclasses import dataclass

from .texture import Texture
from ...linalg import Matrix
from ...rendering import Frame


@dataclass
class ShaderContext:
    model_matrix: Matrix
    view_matrix: Matrix
    projection_matrix: Matrix
    frame: Frame
    texture: Texture
