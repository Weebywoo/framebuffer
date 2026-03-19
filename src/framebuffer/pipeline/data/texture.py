from __future__ import annotations

from dataclasses import dataclass

import numpy
from PIL import Image
from PIL.ImageFile import ImageFile

from framebuffer.linalg import Vector


@dataclass
class Texture:
    texture: list[list[list[int]]]
    width: int
    height: int

    def sample(self, coordinates: Vector) -> Vector:
        u: float = coordinates.x % 1.0
        v: float = coordinates.y % 1.0
        x: int = int(u * (self.width - 1))
        y: int = int(v * (self.height - 1))
        color: list[int] = self.texture[y][x]

        if len(color) == 3:
            return Vector(color + [255])

        return Vector(color)

    @classmethod
    def load(cls, filepath: str) -> Texture:
        image: ImageFile = Image.open(filepath)

        return Texture(width=image.width, height=image.height, texture=numpy.array(image).tolist())
