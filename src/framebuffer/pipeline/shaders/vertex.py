from ..data import Vertex, ShaderContext
from ...linalg import Vector


def default_vertex_shader(vertex: Vertex, /, ctx: ShaderContext) -> Vertex:
    position_model: Vector = Vector([vertex.position.x, vertex.position.y, vertex.position.z, 1.0])
    position_world: Vector = ctx.model_matrix @ position_model
    position_view: Vector = ctx.view_matrix @ position_world
    position_clip: Vector = ctx.projection_matrix @ position_view

    return Vertex(position=position_clip, uv=vertex.uv, normal=vertex.normal)
