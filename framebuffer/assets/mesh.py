from __future__ import annotations

from dataclasses import dataclass

from framebuffer.pipeline.data.vertex import Vertex


@dataclass
class Mesh:
    vertices: list[Vertex]
    indices: list[int]
