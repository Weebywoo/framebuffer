from dataclasses import dataclass

from .texture import Texture
from ...linalg import Vector


@dataclass
class Fragment:
    position: Vector
    depth: float
    uv: Vector
    texture: Texture
