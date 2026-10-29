import numba
import numpy

from framebuffer.math.linalg import Vector


@numba.jit(nopython=True)
# TODO [severity 3/5, effort 3/5]: Cache shared viewport mappings per draw.
def viewport_mapping(vertex: Vector[numpy.float64], dimensions: Vector[numpy.uint16]) -> Vector[numpy.float64]:
    if vertex[3] == 0.0:
        raise ValueError("viewport_mapping: vertex->position->w must be non-zero")

    inverted_w: float = 1.0 / vertex[3]
    ndc_x: float = vertex[0] * inverted_w
    ndc_y: float = vertex[1] * inverted_w
    ndc_z: float = vertex[2] * inverted_w
    screen_x: float = (ndc_x * 0.5 + 0.5) * (dimensions[0] - 1)
    screen_y: float = (1 - (ndc_y * 0.5 + 0.5)) * (dimensions[1] - 1)

    return numpy.array(
        [
            screen_x,
            screen_y,
            ndc_z,
            vertex[3],
            *vertex[4:6],
            *vertex[6:9],
            ndc_z,
            inverted_w,
        ],
        dtype=numpy.float64,
    )
