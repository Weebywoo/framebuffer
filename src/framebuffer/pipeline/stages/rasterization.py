from typing import Generator, Any

from ..data import Fragment, Texture, Triangle, Vertex
from ...linalg import Vector
from ...linalg.utils import (
    signed_triangle_area,
    calc_2d_aabb,
    point_in_triangle,
    calc_barycentric_weights,
)


def rasterize(
    triangle: Triangle[Vertex],
    dimensions: tuple[int, int],
    texture: Texture,
) -> Generator[Fragment, Any, None]:
    vertex_0, vertex_1, vertex_2 = triangle
    triangle_area: float = signed_triangle_area(
        a=Vector([vertex_0.position.x, vertex_0.position.y]),
        b=Vector([vertex_1.position.x, vertex_1.position.y]),
        c=Vector([vertex_2.position.x, vertex_2.position.y]),
    )

    if triangle_area >= 0.0:
        return

    x_start, y_start, x_end, y_end = calc_2d_aabb(
        vertices=(vertex_0.position, vertex_1.position, vertex_2.position),
        dimensions=dimensions,
    )

    for y in range(y_start, y_end + 1, 1):
        for x in range(x_start, x_end + 1, 1):
            point: Vector = Vector([x, y])
            in_triangle, triangle_areas = point_in_triangle(
                vertices=(vertex_0.position, vertex_1.position, vertex_2.position),
                point=point,
            )

            if not in_triangle:
                continue

            weights: Vector = calc_barycentric_weights(*triangle_areas)
            inverted_w: float = weights.dot(
                Vector(
                    [
                        vertex_0.inverted_w,
                        vertex_1.inverted_w,
                        vertex_2.inverted_w,
                    ]
                )
            )

            if inverted_w == 0.0:
                continue

            uv_0: Vector = vertex_0.uv * vertex_0.inverted_w * weights.x
            uv_1: Vector = vertex_1.uv * vertex_1.inverted_w * weights.y
            uv_2: Vector = vertex_2.uv * vertex_2.inverted_w * weights.z
            uv: Vector = (uv_0 + uv_1 + uv_2) * (1.0 / inverted_w)
            depth: float = weights.dot(Vector([vertex_0.depth, vertex_1.depth, vertex_2.depth]))

            yield Fragment(position=point, depth=depth, texture=texture, uv=uv)
