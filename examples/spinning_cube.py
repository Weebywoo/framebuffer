import math

from .io_utils import load_obj
from framebuffer.linalg import Vector3
from framebuffer.pipeline.data import Texture, Vertex

clipping: tuple[float, float] = (1.0, 20.0)
camera_position: Vector3 = Vector3(x=0, y=0, z=-5)
camera_fow: float = math.radians(60)
vertex_buffer_cube, index_buffers_cube = load_obj("./resources/models/cube.obj")
vertex_buffers_plane, index_buffers_plane = load_obj("./resources/models/plane.obj")
vertex_buffers: list[list[Vertex]] = [vertex_buffer_cube, vertex_buffers_plane]
index_buffers: list[list[int]] = [index_buffers_cube, index_buffers_plane]
textures: list[Texture] = [
    Texture.load(filepath="./resources/textures/cat_texture.jpg"),
    Texture.load(filepath="./resources/textures/CustomUVChecker_byValle_8K.png"),
]
mesh_positions: list[Vector3] = [Vector3.zeros(), Vector3(x=0, y=-2, z=0)]
mesh_scales: list[Vector3] = [Vector3.ones(), Vector3.ones()]
mesh_rotations: list[Vector3] = [Vector3.zeros(), Vector3.zeros()]
