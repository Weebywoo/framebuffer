from ..data import Vertex
from ...linalg import Vector4


def viewport_mapping(vertex: Vertex, dimensions: tuple[int, int]) -> Vertex:
    if vertex.position.w == 0.0:
        raise ValueError("viewport_mapping: vertex.position.w must be non-zero")

    inverted_w: float = 1.0 / vertex.position.w
    ndc_x: float = vertex.position.x * inverted_w
    ndc_y: float = vertex.position.y * inverted_w
    ndc_z: float = vertex.position.z * inverted_w
    screen_x: float = (ndc_x * 0.5 + 0.5) * (dimensions[0] - 1)
    screen_y: float = (1 - (ndc_y * 0.5 + 0.5)) * (dimensions[1] - 1)

    mapped: Vertex = Vertex(
        position=Vector4(screen_x, screen_y, ndc_z, vertex.position.w),
        uv=vertex.uv,
        depth=ndc_z,
        inverted_w=inverted_w,
        normal=vertex.normal,
    )

    return mapped
