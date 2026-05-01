from contextlib import contextmanager
from typing import Generator, Any

from .backend import Backend
from .frame import Frame
from ..linalg import Vector
from ..pipeline.data import ShaderContext, Vertex, Triangle
from ..pipeline.shaders import default_vertex_shader, default_fragment_shader
from ..pipeline.stages import primitive_assembly, rasterize, viewport_mapping, clip_triangle


class Renderer:
    def __init__(self) -> None:
        self._backend: Backend = Backend()
        self._frame: Frame = Frame(size=self._backend.get_size())

    @staticmethod
    def draw(vertex_buffer: list[Vertex], index_buffer: list[int], ctx: ShaderContext) -> None:
        # Vertex Shader
        transformed_vertices: list[Vertex] = [default_vertex_shader(vertex, ctx=ctx) for vertex in vertex_buffer]
        # Primitive assembly
        triangles: list[Triangle[Vertex]] = primitive_assembly(transformed_vertices, index_buffer)

        for triangle in triangles:
            clipped_triangles: list[Triangle[Vertex]] = clip_triangle(triangle, clipping=ctx.clipping)

            for clipped_triangle in clipped_triangles:
                mapped_triangle: Triangle[Vertex] = (
                    viewport_mapping(clipped_triangle[0], dimensions=ctx.frame.size),
                    viewport_mapping(clipped_triangle[1], dimensions=ctx.frame.size),
                    viewport_mapping(clipped_triangle[2], dimensions=ctx.frame.size),
                )

                # Rasterizer
                for fragment in rasterize(mapped_triangle, dimensions=ctx.frame.size):
                    if ctx.frame.compare_depth(fragment.position, fragment.depth):
                        # Fragment Shader
                        color: Vector = default_fragment_shader(fragment, ctx=ctx)
                        ctx.frame.draw_pixel(fragment.position, color, fragment.depth)

    @contextmanager
    def frame(self) -> Generator[Frame, Any, None]:
        self._frame.set_size(self._backend.get_size())
        self._frame.clear()

        yield self._frame

        self._backend.present(self._frame)
