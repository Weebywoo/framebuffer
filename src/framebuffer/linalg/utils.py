import math

from .vector import Vector


def point_in_triangle(
    vertices: tuple[Vector, Vector, Vector], point: Vector
) -> tuple[bool, tuple[float, float, float]]:
    a: Vector = Vector([vertices[0].x, vertices[0].y])
    b: Vector = Vector([vertices[1].x, vertices[1].y])
    c: Vector = Vector([vertices[2].x, vertices[2].y])
    area_ABP: float = signed_triangle_area(a, b, point)
    area_BCP: float = signed_triangle_area(b, c, point)
    area_CAP: float = signed_triangle_area(c, a, point)
    has_pos: bool = area_ABP > 0 or area_BCP > 0 or area_CAP > 0
    has_neg: bool = area_ABP < 0 or area_BCP < 0 or area_CAP < 0
    in_triangle: bool = not (has_pos and has_neg) and area_ABP + area_BCP + area_CAP != 0.0

    return in_triangle, (area_ABP, area_BCP, area_CAP)


def signed_triangle_area(a: Vector, b: Vector, c: Vector) -> float:
    ac: Vector = c - a
    ab: Vector = b - a
    ab_perpendicular: Vector = Vector([ab.y, -ab.x])

    return ac.dot(ab_perpendicular) / 2


def calc_barycentric_weights(area_ABP: float, area_BCP: float, area_CAP: float) -> Vector:
    inverse_area_sum: float = 1 / (area_ABP + area_BCP + area_CAP)

    return Vector(
        [
            area_BCP * inverse_area_sum,
            area_CAP * inverse_area_sum,
            area_ABP * inverse_area_sum,
        ]
    )


def clamp(a: int, vmin: int = 0, vmax: int = 1) -> int:
    return max(min(a, vmax), vmin)


def calc_2d_aabb(vertices: tuple[Vector, Vector, Vector], dimensions: tuple[int, int]) -> tuple[int, int, int, int]:
    a, b, c = vertices
    width, height = dimensions
    min_x: float = min(a.x, b.x, c.x)
    min_y: float = min(a.y, b.y, c.y)
    max_x: float = max(a.x, b.x, c.x)
    max_y: float = max(a.y, b.y, c.y)
    BB_start_x: int = clamp(math.floor(min_x), 0, width - 1)
    BB_start_y: int = clamp(math.floor(min_y), 0, height - 1)
    BB_end_x: int = clamp(math.ceil(max_x), 0, width - 1)
    BB_end_y: int = clamp(math.ceil(max_y), 0, height - 1)

    return BB_start_x, BB_start_y, BB_end_x, BB_end_y
