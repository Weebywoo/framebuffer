from typing import Generator

import numba
import numpy

from framebuffer.math.linalg import Vector, lerp


@numba.jit(nopython=True)
# TODO [severity 2/5, effort 2/5]: Reuse signed clip-plane distances.
def lerp_vertices(
    vertex_a: Vector[numpy.float64],
    vertex_b: Vector[numpy.float64],
) -> Vector[numpy.float64]:
    fraction: numpy.float64 = -vertex_a[2] / (vertex_b[2] - vertex_a[2])

    return lerp(vertex_a, vertex_b, fraction)


@numba.jit(nopython=True)
# TODO [severity 2/5, effort 3/5]: Reject triangles outside the frustum early.
# TODO [severity 4/5, effort 3/5]: Clip against all six homogeneous frustum planes.
def clip_triangle(vertices: Vector[numpy.float64]) -> Generator[Vector[numpy.float64], None, None]:
    vertex_0, vertex_1, vertex_2 = vertices[:11], vertices[11:22], vertices[22:]

    vertex_0_clip: bool = vertex_0[2] < 0.0
    vertex_1_clip: bool = vertex_1[2] < 0.0
    vertex_2_clip: bool = vertex_2[2] < 0.0
    index: int = 0 if vertex_0_clip else 1 if vertex_1_clip else 2
    index_next: int = (index + 1) % 3
    index_previous: int = (index - 1) % 3

    match int(vertex_0_clip) + int(vertex_1_clip) + int(vertex_2_clip):
        case 0:
            yield vertices

        case 1:
            vertex_edge_a: Vector[numpy.float64] = lerp_vertices(
                vertices[index * 11 : (index + 1) * 11],
                vertices[index_previous * 11 : (index_previous + 1) * 11],
            )
            vertex_edge_b: Vector[numpy.float64] = lerp_vertices(
                vertices[index * 11 : (index + 1) * 11],
                vertices[index_next * 11 : (index_next + 1) * 11],
            )

            yield numpy.array(
                [
                    *vertices[index_previous * 11 : (index_previous + 1) * 11],
                    *vertex_edge_a,
                    *vertices[index_next * 11 : (index_next + 1) * 11],
                ]
            )
            yield numpy.array(
                [
                    *vertex_edge_a,
                    *vertex_edge_b,
                    *vertices[index_next * 11 : (index_next + 1) * 11],
                ]
            )

        case 2:
            inside: int = 0 if not vertex_0_clip else 1 if not vertex_1_clip else 2
            previous_index: int = (inside - 1) % 3
            next_index: int = (inside + 1) % 3
            edge_a: Vector[numpy.float64] = lerp_vertices(
                vertices[inside * 11 : (inside + 1) * 11],
                vertices[previous_index * 11 : (previous_index + 1) * 11],
            )
            edge_b: Vector[numpy.float64] = lerp_vertices(
                vertices[inside * 11 : (inside + 1) * 11],
                vertices[next_index * 11 : (next_index + 1) * 11],
            )

            yield numpy.array([*vertices[inside * 11 : (inside + 1) * 11], *edge_b, *edge_a])
