from ..data import Fragment, ShaderContext
from ...linalg import Vector


def default_fragment_shader(fragment: Fragment, /, ctx: ShaderContext) -> Vector:
    return fragment.texture.sample(fragment.uv)
