import numba
import numpy

from framebuffer.math.linalg import Matrix, Vector, MatrixNDIM
from framebuffer.pipeline.shaders.fragment_shader import fragment_shader
from framebuffer.pipeline.shaders.vertex_shader import vertex_shader
from framebuffer.pipeline.stages.assembly import primitive_assembly
from framebuffer.pipeline.stages.clipping import clip_triangle
from framebuffer.pipeline.stages.rasterization import rasterize
from framebuffer.pipeline.stages.viewport import viewport_mapping


@numba.jit(nopython=True)
def render_vertex_buffer(
    vertex_buffer: Vector[numpy.float64],
    index_buffer: Vector[numpy.uint32],
    /,
    texture: MatrixNDIM[numpy.uint8],
    frame_size: Vector[numpy.uint16],
    color_buffer: MatrixNDIM[numpy.uint8],
    depth_buffer: Matrix[numpy.float64],
    model_matrix: Matrix[numpy.float64],
    view_matrix: Matrix[numpy.float64],
    projection_matrix: Matrix[numpy.float64],
) -> None:
    # Vertex Shader
    transformed_vertex_buffer: Vector[numpy.float64] = vertex_buffer.copy()
    for vindex in range(0, len(vertex_buffer), 11):
        transformed_vertex_buffer[vindex : vindex + 4] = vertex_shader(
            vertex_buffer[vindex : vindex + 4],
            model_matrix=model_matrix,
            view_matrix=view_matrix,
            projection_matrix=projection_matrix,
        )

    # Primitive assembly
    for triangle in primitive_assembly(transformed_vertex_buffer, index_buffer):
        # Triangle clipping
        for clipped_triangle in clip_triangle(triangle):
            vertex_0, vertex_1, vertex_2 = clipped_triangle[:11], clipped_triangle[11:22], clipped_triangle[22:]
            mapped_triangle: Vector[numpy.float64] = numpy.array(
                [
                    *viewport_mapping(vertex_0, dimensions=frame_size),
                    *viewport_mapping(vertex_1, dimensions=frame_size),
                    *viewport_mapping(vertex_2, dimensions=frame_size),
                ]
            )

            # Rasterizer
            for fragment in rasterize(mapped_triangle, dimensions=frame_size, depth_buffer=depth_buffer):
                x, y = int(fragment[0]), int(fragment[1])
                # Fragment Shader
                color_buffer[y][x] = fragment_shader(fragment, texture=texture)
                depth_buffer[y][x] = fragment[4]
