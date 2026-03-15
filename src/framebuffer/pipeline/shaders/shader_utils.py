import math

from ...linalg import Matrix4x4, Vector3


def create_model_matrix(scale: Vector3, rotation: Vector3, position: Vector3) -> Matrix4x4:
    scaling_matrix: Matrix4x4 = Matrix4x4.zeros()
    scaling_matrix[0, 0] = scale.x
    scaling_matrix[1, 1] = scale.y
    scaling_matrix[2, 2] = scale.z
    scaling_matrix[3, 3] = 1.0

    pitch: Matrix4x4 = Matrix4x4.zeros()
    pitch[0, 0] = 1.0
    pitch[1, 1] = math.cos(rotation.x)
    pitch[1, 2] = -math.sin(rotation.x)
    pitch[2, 1] = math.sin(rotation.x)
    pitch[2, 2] = math.cos(rotation.x)
    pitch[3, 3] = 1.0

    yaw: Matrix4x4 = Matrix4x4.zeros()
    yaw[0, 0] = math.cos(rotation.y)
    yaw[0, 2] = -math.sin(rotation.y)
    yaw[1, 1] = 1.0
    yaw[2, 0] = math.sin(rotation.y)
    yaw[2, 2] = math.cos(rotation.y)
    yaw[3, 3] = 1.0

    roll: Matrix4x4 = Matrix4x4.zeros()
    roll[0, 0] = math.cos(rotation.z)
    roll[0, 1] = -math.sin(rotation.z)
    roll[1, 0] = math.sin(rotation.z)
    roll[1, 1] = math.cos(rotation.z)
    roll[2, 2] = 1.0
    roll[3, 3] = 1.0
    rotation_matrix: Matrix4x4 = roll @ yaw @ pitch

    translation_matrix: Matrix4x4 = Matrix4x4.zeros()
    translation_matrix[0, 0] = 1.0
    translation_matrix[1, 1] = 1.0
    translation_matrix[2, 2] = 1.0
    translation_matrix[3, 3] = 1.0
    translation_matrix[0, 3] = position.x
    translation_matrix[1, 3] = position.y
    translation_matrix[2, 3] = position.z

    return translation_matrix @ rotation_matrix @ scaling_matrix


def create_view_matrix(camera_position: Vector3, camera_rotation: Vector3) -> Matrix4x4:
    up: Vector3 = Vector3(x=0.0, y=1.0, z=0.0)
    f: Vector3 = Vector3(
        x=math.cos(camera_rotation.x) * math.sin(camera_rotation.y),
        y=math.sin(camera_rotation.x),
        z=math.cos(camera_rotation.x) * math.cos(camera_rotation.y),
    ).normalised
    s: Vector3 = up.cross(f).normalised
    u: Vector3 = f.cross(s)

    return Matrix4x4(
        [
            [s.x, s.y, s.z, -s.dot(camera_position)],
            [u.x, u.y, u.z, -u.dot(camera_position)],
            [f.x, f.y, f.z, -f.dot(camera_position)],
            [0.0, 0.0, 0.0, 1.0],
        ]
    )


def create_projection_matrix(aspect_ratio: float, fov: float, clipping: tuple[float, float]) -> Matrix4x4:
    near, far = clipping
    f: float = 1.0 / math.tan(fov / 2.0)

    return Matrix4x4(
        [
            [f / aspect_ratio, 0.0, 0.0, 0.0],
            [0.0, f, 0.0, 0.0],
            [0.0, 0.0, far / (far - near), (-near * far) / (far - near)],
            [0.0, 0.0, 1.0, 0.0],
        ]
    )
