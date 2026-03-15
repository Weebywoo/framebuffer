from dataclasses import dataclass

from .texture import Texture
from ...linalg import Matrix4x4
from ...rendering import Frame


@dataclass
class ShaderContext:
    model_matrix: Matrix4x4
    view_matrix: Matrix4x4
    projection_matrix: Matrix4x4
    frame: Frame
    texture: Texture
