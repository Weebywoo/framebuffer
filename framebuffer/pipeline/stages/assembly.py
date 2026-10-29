from typing import Any, Generator

import numba
import numpy

from framebuffer.math.linalg import Vector


@numba.jit(nopython=True)
# TODO [severity 3/5, effort 2/5]: Centralize packed vertex strides and attribute offsets.
def primitive_assembly(
    vertex_buffer: Vector[numpy.float64], index_buffer: Vector[numpy.uint32]
) -> Generator[Vector[numpy.float64], Any, None]:
    for ibuffer_index in range(0, len(index_buffer), 3):
        triangle: Vector[numpy.float64] = numpy.empty(33, dtype=numpy.float64)

        for slot in range(3):
            vertex_index: int = int(index_buffer[ibuffer_index + slot]) * 11
            triangle[slot * 11 : (slot + 1) * 11] = vertex_buffer[vertex_index : vertex_index + 11]

        yield triangle
