from dataclasses import dataclass

from .texture import Texture
from ...linalg import Vector2


@dataclass
class Fragment:
    position: Vector2
    depth: float
    uv: Vector2
    texture: Texture
