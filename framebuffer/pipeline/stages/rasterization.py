from typing import Any, Generator

import numba
import numpy

from framebuffer.math.linalg import (
    calc_2d_aabb,
    point_in_triangle,
    signed_triangle_area,
    Vector,
    Matrix,
)


@numba.jit(nopython=True, boundscheck=True)
# TODO [severity 5/5, effort 4/5]: Step edge and attribute planes with integer loops.
def rasterize(
    triangle: Vector[numpy.float64],
    dimensions: Vector[numpy.uint16],
    depth_buffer: Matrix[numpy.float64],
) -> Generator[Vector[numpy.float64], Any, None]:
    vertex_0, vertex_1, vertex_2 = triangle[:11], triangle[11:22], triangle[22:]
    triangle_area: float = signed_triangle_area(
        a=vertex_0[0:2],
        b=vertex_1[0:2],
        c=vertex_2[0:2],
    )

    if triangle_area >= 0.0:
        return

    x_start, y_start, x_end, y_end = calc_2d_aabb(
        position_0=vertex_0[0:2],
        position_1=vertex_1[0:2],
        position_2=vertex_2[0:2],
        dimensions=dimensions,
    )
    inverse_area: float = 1.0 / triangle_area

    for y in numpy.arange(y_start, y_end + 1, 1, dtype=numpy.uint16):
        for x in numpy.arange(x_start, x_end + 1, 1, dtype=numpy.uint16):
            point: Vector[numpy.uint16] = numpy.array([x, y])
            triangle_result: Vector[numpy.float64] = point_in_triangle(
                position_0=vertex_0[0:2],
                position_1=vertex_1[0:2],
                position_2=vertex_2[0:2],
                point=point,
            )
            in_triangle: float = triangle_result[0]
            triangle_areas: Vector[numpy.float64] = triangle_result[1:4]

            if not bool(in_triangle):
                continue

            # calculate barycentric weights
            weight_0: numpy.float64 = triangle_areas[1] * inverse_area
            weight_1: numpy.float64 = triangle_areas[2] * inverse_area
            weight_2: numpy.float64 = triangle_areas[0] * inverse_area
            inverted_w: float = weight_0 * vertex_0[10] + weight_1 * vertex_1[10] + weight_2 * vertex_2[10]

            if inverted_w == 0.0:
                continue

            depth: float = weight_0 * vertex_0[9] + weight_1 * vertex_1[9] + weight_2 * vertex_2[9]

            if not (depth < depth_buffer[y][x]):
                continue

            uv_0: Vector[numpy.float64] = vertex_0[4:6] * vertex_0[10] * weight_0
            uv_1: Vector[numpy.float64] = vertex_1[4:6] * vertex_1[10] * weight_1
            uv_2: Vector[numpy.float64] = vertex_2[4:6] * vertex_2[10] * weight_2
            uv: Vector[numpy.float64] = (uv_0 + uv_1 + uv_2) * (1.0 / inverted_w)

            yield numpy.array([*point, *uv, depth])
