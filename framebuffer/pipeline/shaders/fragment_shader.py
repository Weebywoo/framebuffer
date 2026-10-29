import numba
import numpy

from framebuffer.math.linalg import MatrixNDIM, Vector


@numba.jit(nopython=True)
def fragment_shader(fragment: Vector[numpy.float64], /, texture: MatrixNDIM[numpy.uint8]) -> Vector[numpy.uint8]:
    u: float = fragment[2] % 1.0
    v: float = fragment[3] % 1.0
    height, width = texture.shape[:2]
    x: int = int(u * (width - 1))
    y: int = int(v * (height - 1))

    return texture[y][x][:3]
