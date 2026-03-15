from ..data import Vertex, ShaderContext
from ...linalg import Vector4


def default_vertex_shader(vertex: Vertex, /, ctx: ShaderContext) -> Vertex:
    position_model: Vector4 = Vector4(x=vertex.position.x, y=vertex.position.y, z=vertex.position.z, w=1.0)
    position_world: Vector4 = ctx.model_matrix @ position_model
    position_view: Vector4 = ctx.view_matrix @ position_world
    position_clip: Vector4 = ctx.projection_matrix @ position_view

    return Vertex(position=position_clip, uv=vertex.uv, normal=vertex.normal)
