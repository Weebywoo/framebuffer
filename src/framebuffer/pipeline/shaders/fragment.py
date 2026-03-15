from ..data import Fragment, ShaderContext
from ...linalg import Vector4


def default_fragment_shader(fragment: Fragment, /, ctx: ShaderContext) -> Vector4:
    return fragment.texture.sample(fragment.uv)
