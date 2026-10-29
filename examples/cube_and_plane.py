import math
import os
from pathlib import Path

import numpy

from framebuffer.components.transform_component import TransformComponent
from framebuffer.engine import GameEngine
from framebuffer.scene.camera import Camera
from framebuffer.scene.entity import Entity
from framebuffer.scene.model import Model
from framebuffer.scene.scene import Scene
from framebuffer.scene.transform import Transform


def main() -> None:
    assets = Path(__file__).resolve().parent / "assets"
    entities: list[Entity] = [
        Model.load(
            mesh_filepath=str(assets / "models" / "cube.obj"),
            texture_filepath=str(assets / "textures" / "cat_texture.jpg"),
            components=[TransformComponent(rotation=numpy.array([0.15, 0.05, 0.1]))],
        ),
        Model.load(
            mesh_filepath=str(assets / "models" / "plane.obj"),
            texture_filepath=str(assets / "textures" / "UVCheck_byValle.png"),
            transform=Transform(position=numpy.array([0, -2, 0], dtype=numpy.float64)),
        ),
        Camera(
            fov=math.radians(60),
            clipping=numpy.array([1.0, 20.0]),
            transform=Transform(position=numpy.array([0, 0, -5], dtype=numpy.float64)),
        ),
    ]
    scene: Scene = Scene(entities=entities)
    GameEngine(scene).run()


if __name__ == "__main__":
    os.system("cls")

    try:
        main()

    except KeyboardInterrupt:
        os.system("cls")
        pass
