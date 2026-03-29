from ..data import Vertex, ShaderContext
from ...linalg import Vector


def default_vertex_shader(vertex: Vertex, /, ctx: ShaderContext) -> Vertex:
    position_model: Vector = Vector([vertex.position.x, vertex.position.y, vertex.position.z, 1.0])
    position_world: Vector = position_model @ ctx.model_matrix
    position_view: Vector = position_world @ ctx.view_matrix
    position_clip: Vector = position_view @ ctx.projection_matrix

    return Vertex(position=position_clip, uv=vertex.uv, normal=vertex.normal)
