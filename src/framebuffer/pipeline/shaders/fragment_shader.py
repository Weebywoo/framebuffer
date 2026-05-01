from ..data import Fragment, ShaderContext
from ...linalg import Vector


def default_fragment_shader(fragment: Fragment, /, ctx: ShaderContext) -> Vector:
    u: float = fragment.uv.u % 1.0
    v: float = fragment.uv.v % 1.0
    x: int = int(u * (ctx.texture_shape[0] - 1))
    y: int = int(v * (ctx.texture_shape[1] - 1))
    color: list[int] = ctx.texture[y][x]

    if len(color) == 3:
        return Vector(color + [255])

    return Vector(color)
