from ..data import Triangle, Vertex


def clip_triangle(triangle: Triangle[Vertex]) -> list[Triangle[Vertex]] | None:
    for vertex in triangle:
        w: float = vertex.position.w
        z: float = vertex.position.z

        if w <= 0.0:
            return None

        if z < 0.0 or z > w:
            return None

    return [triangle]
