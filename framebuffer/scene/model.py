from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional, Any

import numpy

from framebuffer.scene.entity import Entity
from framebuffer.assets.mesh import Mesh
from .transform import Transform
from framebuffer.assets.loaders import ImageLoader, MeshLoader
from framebuffer.math.linalg import MatrixNDIM

if TYPE_CHECKING:
    from framebuffer.components.base_component import BaseComponent


@dataclass(kw_only=True)
class Model(Entity):
    mesh: Mesh
    texture: MatrixNDIM[numpy.uint8]

    @classmethod
    # TODO [severity 2/5, effort 2/5]: Cache shared meshes and textures by asset path.
    def load(
        cls,
        mesh_filepath: str,
        texture_filepath: str,
        transform: Optional[Transform] = None,
        components: Optional[list[BaseComponent]] = None,
    ) -> Model:
        kwargs: dict[str, Any] = {
            "mesh": Mesh(*MeshLoader.load(mesh_filepath)),
            "texture": ImageLoader.load(texture_filepath),
        }

        if transform is not None:
            kwargs["transform"] = transform

        if components is not None:
            kwargs["components"] = components

        return cls(**kwargs)
