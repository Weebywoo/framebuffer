from contextlib import contextmanager
from typing import Any, Generator

import numpy

from framebuffer.math.linalg import Vector
from framebuffer.pipeline.data.shader_context import ShaderContext
from framebuffer.pipeline.data.vertex import Vertex

from .backend import Backend
from .frame import Frame
from .render_vertex_buffer import render_vertex_buffer


class Renderer:
    def __init__(self) -> None:
        self._backend: Backend = Backend()
        self._frame: Frame = Frame(size=self._backend.get_size())

    @property
    def screen_size(self) -> Vector[numpy.uint16]:
        return self._frame.size

    @staticmethod
    # TODO [severity 4/5, effort 2/5]: Validate vertex layouts and index ranges before entering Numba.
    def draw(vertex_buffer: list[Vertex], index_buffer: list[int], ctx: ShaderContext) -> None:
        vectorized_vertex_buffer: Vector[numpy.float64] = numpy.array(
            [
                [*vertex.position, *vertex.uv, *vertex.normal, vertex.depth, vertex.inverted_w]
                for vertex in vertex_buffer
            ]
        ).flatten()

        render_vertex_buffer(
            vectorized_vertex_buffer,
            numpy.asarray(index_buffer, dtype=numpy.uint32),
            texture=ctx.texture,
            frame_size=ctx.frame.size,
            depth_buffer=ctx.frame.depth_buffer,
            color_buffer=ctx.frame.color_buffer,
            model_matrix=ctx.model_matrix,
            view_matrix=ctx.view_matrix,
            projection_matrix=ctx.projection_matrix,
        )

    @contextmanager
    def frame(self) -> Generator[Frame, Any, None]:
        self._frame.set_size(self._backend.get_size())

        self._frame.clear()

        yield self._frame

        self._backend.present(self._frame)
