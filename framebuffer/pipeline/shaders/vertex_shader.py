import numba
import numpy

from framebuffer.math.linalg import Vector, Matrix


@numba.jit(nopython=True)
# TODO [severity 3/5, effort 3/5]: Combine matrices per draw; batch vertex transforms.
def vertex_shader(
    vertex: Vector[numpy.float64],
    /,
    model_matrix: Matrix[numpy.float64],
    view_matrix: Matrix[numpy.float64],
    projection_matrix: Matrix[numpy.float64],
) -> Vector[numpy.float64]:
    return vertex @ model_matrix @ view_matrix @ projection_matrix
