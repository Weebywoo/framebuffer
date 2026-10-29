import math

import numba
import numpy

from framebuffer.math.linalg import Vector, Matrix


@numba.jit(nopython=True)
# TODO [severity 2/5, effort 2/5]: Cache model matrices until transforms change.
def create_model_matrix(
    scale: Vector[numpy.float64],
    rotation: Vector[numpy.float64],
    position: Vector[numpy.float64],
) -> Matrix[numpy.float64]:
    scaling_matrix: Matrix[numpy.float64] = numpy.zeros((4, 4))
    scaling_matrix[0, 0] = scale[0]
    scaling_matrix[1, 1] = scale[1]
    scaling_matrix[2, 2] = scale[2]
    scaling_matrix[3, 3] = 1.0

    pitch: Matrix[numpy.float64] = numpy.zeros((4, 4))
    pitch[0, 0] = 1.0
    pitch[1, 1] = math.cos(rotation[0])
    pitch[2, 1] = math.sin(rotation[0])
    pitch[1, 2] = -math.sin(rotation[0])
    pitch[2, 2] = math.cos(rotation[0])
    pitch[3, 3] = 1.0

    yaw: Matrix[numpy.float64] = numpy.zeros((4, 4))
    yaw[0, 0] = math.cos(rotation[1])
    yaw[2, 0] = -math.sin(rotation[1])
    yaw[1, 1] = 1.0
    yaw[0, 2] = math.sin(rotation[1])
    yaw[2, 2] = math.cos(rotation[1])
    yaw[3, 3] = 1.0

    roll: Matrix[numpy.float64] = numpy.zeros((4, 4))
    roll[0, 0] = math.cos(rotation[2])
    roll[1, 0] = math.sin(rotation[2])
    roll[0, 1] = -math.sin(rotation[2])
    roll[1, 1] = math.cos(rotation[2])
    roll[2, 2] = 1.0
    roll[3, 3] = 1.0
    rotation_matrix: Matrix[numpy.float64] = roll @ yaw @ pitch

    translation_matrix: Matrix[numpy.float64] = numpy.zeros((4, 4))
    translation_matrix[0, 0] = 1.0
    translation_matrix[1, 1] = 1.0
    translation_matrix[2, 2] = 1.0
    translation_matrix[3, 3] = 1.0
    translation_matrix[3, 0] = position[0]
    translation_matrix[3, 1] = position[1]
    translation_matrix[3, 2] = position[2]

    return translation_matrix @ rotation_matrix @ scaling_matrix


@numba.jit(nopython=True)
# TODO [severity 2/5, effort 2/5]: Cache the view matrix until the camera changes.
def create_view_matrix(
    camera_position: Vector[numpy.float64],
    camera_rotation: Vector[numpy.float64],
) -> Matrix[numpy.float64]:
    up: Vector[numpy.float64] = numpy.array([0.0, 1.0, 0.0])
    f: Vector[numpy.float64] = numpy.array(
        [
            math.cos(camera_rotation[0]) * math.sin(camera_rotation[1]),
            math.sin(camera_rotation[0]),
            math.cos(camera_rotation[0]) * math.cos(camera_rotation[1]),
        ]
    )
    f /= numpy.linalg.norm(f)
    s: Vector[numpy.float64] = numpy.cross(up, f)
    s /= numpy.linalg.norm(s)
    u: Vector[numpy.float64] = numpy.cross(f, s)
    matrix: Matrix[numpy.float64] = numpy.zeros((4, 4))
    matrix[0, 0] = s[0]
    matrix[1, 0] = s[1]
    matrix[2, 0] = s[2]
    matrix[3, 0] = -s.dot(camera_position)
    matrix[0, 1] = u[0]
    matrix[1, 1] = u[1]
    matrix[2, 1] = u[2]
    matrix[3, 1] = -u.dot(camera_position)
    matrix[0, 2] = f[0]
    matrix[1, 2] = f[1]
    matrix[2, 2] = f[2]
    matrix[3, 2] = -f.dot(camera_position)
    matrix[3, 3] = 1.0

    return matrix


@numba.jit(nopython=True)
# TODO [severity 2/5, effort 2/5]: Cache projection by aspect ratio, FOV, and clip planes.
def create_projection_matrix(aspect_ratio: float, fov: float, clipping: Vector[numpy.float64]) -> Matrix[numpy.float64]:
    near, far = clipping
    f: float = 1.0 / math.tan(fov / 2.0)
    matrix: Matrix[numpy.float64] = numpy.zeros((4, 4))
    matrix[0, 0] = f / aspect_ratio
    matrix[1, 1] = f
    matrix[2, 2] = far / (far - near)
    matrix[3, 2] = (-near * far) / (far - near)
    matrix[2, 3] = 1.0

    return matrix
