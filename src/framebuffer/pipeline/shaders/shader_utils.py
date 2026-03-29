import math

from ...linalg import Vector, Matrix


def create_model_matrix(scale: Vector, rotation: Vector, position: Vector) -> Matrix:
    scaling_matrix: Matrix = Matrix.zeros((4, 4))
    scaling_matrix[0, 0] = scale.x
    scaling_matrix[1, 1] = scale.y
    scaling_matrix[2, 2] = scale.z
    scaling_matrix[3, 3] = 1.0

    pitch: Matrix = Matrix.zeros((4, 4))
    pitch[0, 0] = 1.0
    pitch[1, 1] = math.cos(rotation.x)
    pitch[2, 1] = math.sin(rotation.x)
    pitch[1, 2] = -math.sin(rotation.x)
    pitch[2, 2] = math.cos(rotation.x)
    pitch[3, 3] = 1.0

    yaw: Matrix = Matrix.zeros((4, 4))
    yaw[0, 0] = math.cos(rotation.y)
    yaw[2, 0] = -math.sin(rotation.y)
    yaw[1, 1] = 1.0
    yaw[0, 2] = math.sin(rotation.y)
    yaw[2, 2] = math.cos(rotation.y)
    yaw[3, 3] = 1.0

    roll: Matrix = Matrix.zeros((4, 4))
    roll[0, 0] = math.cos(rotation.z)
    roll[1, 0] = math.sin(rotation.z)
    roll[0, 1] = -math.sin(rotation.z)
    roll[1, 1] = math.cos(rotation.z)
    roll[2, 2] = 1.0
    roll[3, 3] = 1.0
    rotation_matrix: Matrix = roll @ yaw @ pitch

    translation_matrix: Matrix = Matrix.zeros((4, 4))
    translation_matrix[0, 0] = 1.0
    translation_matrix[1, 1] = 1.0
    translation_matrix[2, 2] = 1.0
    translation_matrix[3, 3] = 1.0
    translation_matrix[3, 0] = position.x
    translation_matrix[3, 1] = position.y
    translation_matrix[3, 2] = position.z

    return translation_matrix @ rotation_matrix @ scaling_matrix


def create_view_matrix(camera_position: Vector, camera_rotation: Vector) -> Matrix:
    up: Vector = Vector([0.0, 1.0, 0.0])
    f: Vector = Vector(
        [
            math.cos(camera_rotation.x) * math.sin(camera_rotation.y),
            math.sin(camera_rotation.x),
            math.cos(camera_rotation.x) * math.cos(camera_rotation.y),
        ]
    ).normalised
    s: Vector = up.cross(f).normalised
    u: Vector = f.cross(s)
    matrix: Matrix = Matrix.zeros((4, 4))
    matrix[0, 0] = s.x
    matrix[1, 0] = s.y
    matrix[2, 0] = s.z
    matrix[3, 0] = -s.dot(camera_position)
    matrix[0, 1] = u.x
    matrix[1, 1] = u.y
    matrix[2, 1] = u.z
    matrix[3, 1] = -u.dot(camera_position)
    matrix[0, 2] = f.x
    matrix[1, 2] = f.y
    matrix[2, 2] = f.z
    matrix[3, 2] = -f.dot(camera_position)
    matrix[3, 3] = 1.0

    return matrix


def create_projection_matrix(aspect_ratio: float, fov: float, clipping: tuple[float, float]) -> Matrix:
    near, far = clipping
    f: float = 1.0 / math.tan(fov / 2.0)
    matrix: Matrix = Matrix.zeros((4, 4))
    matrix[0, 0] = f / aspect_ratio
    matrix[1, 1] = f
    matrix[2, 2] = far / (far - near)
    matrix[3, 2] = (-near * far) / (far - near)
    matrix[2, 3] = 1.0

    return matrix
