import math
import os

from framebuffer import Renderer
from framebuffer.linalg import Vector, Matrix
from framebuffer.pipeline.data import Texture, Vertex, ShaderContext
from framebuffer.pipeline.shaders.shader_utils import create_view_matrix, create_projection_matrix, create_model_matrix
from .io_utils import load_obj


def main() -> None:
    clipping: tuple[float, float] = (1.0, 20.0)
    camera_position: Vector = Vector([0, 0, -5])
    camera_fow: float = math.radians(60)
    vertex_buffer_cube, index_buffers_cube = load_obj("./resources/models/cube.obj")
    vertex_buffers_plane, index_buffers_plane = load_obj("./resources/models/plane.obj")
    vertex_buffers: list[list[Vertex]] = [vertex_buffer_cube, vertex_buffers_plane]
    index_buffers: list[list[int]] = [index_buffers_cube, index_buffers_plane]
    textures: list[Texture] = [
        Texture.load(filepath="./resources/textures/cat_texture.jpg"),
        Texture.load(filepath="./resources/textures/UVCheck_byValle.png"),
    ]
    mesh_positions: list[Vector] = [Vector.zero(3), Vector([0, -2, 0])]
    mesh_scales: list[Vector] = [Vector.fill(1, length=3), Vector.fill(1, length=3)]
    mesh_rotations: list[Vector] = [Vector.zero(3), Vector.zero(3)]

    renderer: Renderer = Renderer()

    for _ in renderer.frames():
        view_matrix: Matrix = create_view_matrix(
            camera_position=camera_position,
            camera_rotation=Vector.zero(3),
        )

        with renderer.frame() as frame:
            projection_matrix: Matrix = create_projection_matrix(
                aspect_ratio=frame.aspect_ratio,
                fov=camera_fow,
                clipping=clipping,
            )

            for vertex_buffer, index_buffer, texture, mesh_position, mesh_scale, mesh_rotation in zip(
                vertex_buffers,
                index_buffers,
                textures,
                mesh_positions,
                mesh_scales,
                mesh_rotations,
            ):
                model_matrix: Matrix = create_model_matrix(
                    scale=Vector.fill(1, length=3),
                    rotation=Vector.zero(3),
                    position=mesh_position,
                )
                shader_context: ShaderContext = ShaderContext(
                    view_matrix=view_matrix,
                    projection_matrix=projection_matrix,
                    model_matrix=model_matrix,
                    frame=frame,
                    texture=texture,
                )

                renderer.draw(vertex_buffer, index_buffer, ctx=shader_context)


if __name__ == "__main__":
    os.system("cls")

    try:
        main()

    except KeyboardInterrupt:
        os.system("cls")
