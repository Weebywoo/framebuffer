from ..data import Triangle, Vertex
from ...linalg import Vector, Matrix, lerp, get_lerp_fraction


def vertex_is_left_of_clip_plane(position: Vector, clipping_plane: tuple[Vector, Vector, Vector, Vector]) -> bool:
    A, B, C, _ = clipping_plane
    BA: Vector = B - A
    CA: Vector = C - A
    PA: Vector = position - A
    matrix: Matrix = Matrix([[*BA], [*CA], [*PA]], shape=(3, 3))

    return matrix.determinant > 0.0


def lerp_vertices(vertex_A: Vertex, vertex_B: Vertex, clipping_distance: float) -> Vertex:
    fraction: float = get_lerp_fraction(vertex_A, vertex_B, clipping_distance)

    return Vertex(
        position=lerp(vertex_A.position, vertex_B.position, fraction),
        uv=lerp(vertex_A.uv, vertex_B.uv, fraction),
        depth=lerp(vertex_A.depth, vertex_B.depth, fraction),
        normal=lerp(vertex_A.normal, vertex_B.normal, fraction),
        inverted_w=lerp(vertex_A.inverted_w, vertex_B.inverted_w, fraction),
    )


def clip_triangle(triangle: Triangle[Vertex], clipping: tuple[float, float]) -> list[Triangle[Vertex]]:
    clipped_triangles: list[Triangle[Vertex]] = []
    vertex_0_clip: bool = triangle[0].position.z <= clipping[0]
    vertex_1_clip: bool = triangle[1].position.z <= clipping[0]
    vertex_2_clip: bool = triangle[2].position.z <= clipping[0]
    index: int = 0 if vertex_0_clip else 1 if vertex_1_clip else 2
    index_next: int = (index + 1) % 3
    index_previous: int = (index - 1) % 3

    match vertex_0_clip + vertex_1_clip + vertex_2_clip:
        case 0:
            clipped_triangles.append(triangle)

        case 1:
            vertex_along_edge_A: Vertex = lerp_vertices(triangle[index], triangle[index_previous], clipping[0])
            vertex_along_edge_B: Vertex = lerp_vertices(triangle[index], triangle[index_next], clipping[0])

            clipped_triangles.append((triangle[index_previous], vertex_along_edge_A, triangle[index_next]))
            clipped_triangles.append((vertex_along_edge_A, vertex_along_edge_B, triangle[index_next]))

        # This case is at fault
        # case 2:
        #     vertex_along_edge_A: Vertex = lerp_vertices(triangle[index], triangle[index_previous], clipping[0])
        #     vertex_along_edge_B: Vertex = lerp_vertices(triangle[index], triangle[index_next], clipping[0])
        #
        #     clipped_triangles.append((triangle[index], vertex_along_edge_A, vertex_along_edge_B))

    return clipped_triangles
