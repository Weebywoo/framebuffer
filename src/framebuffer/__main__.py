import argparse
import importlib
import os
from argparse import Namespace
from types import ModuleType

from framebuffer import Renderer
from framebuffer.linalg import Matrix4x4, Vector3
from framebuffer.pipeline.data import Texture, ShaderContext, Vertex
from framebuffer.pipeline.shaders.shader_utils import create_view_matrix, create_projection_matrix, create_model_matrix


def main() -> None:
    renderer: Renderer = Renderer()

    for _ in renderer.frames():
        view_matrix: "Matrix4x4" = create_view_matrix(
            camera_position=camera_position,
            camera_rotation=Vector3.zeros(),
        )

        with renderer.frame() as frame:
            for vertex_buffer, index_buffer, texture, mesh_position, mesh_scale, mesh_rotation in zip(
                vertex_buffers,
                index_buffers,
                textures,
                mesh_positions,
                mesh_scales,
                mesh_rotations,
            ):
                projection_matrix: "Matrix4x4" = create_projection_matrix(
                    aspect_ratio=frame.aspect_ratio,
                    fov=camera_fow,
                    clipping=clipping,
                )
                model_matrix: "Matrix4x4" = create_model_matrix(
                    scale=Vector3.ones(),
                    rotation=Vector3.zeros(),
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
    try:
        os.system("cls")

        parser: argparse.ArgumentParser = argparse.ArgumentParser()
        parser.add_argument("--example", type=str, action="store", default=None, choices=["spinning_cube"])
        arguments: Namespace = parser.parse_args()

        if arguments.example is None:
            raise Exception("No example specified")

        example: ModuleType = importlib.import_module(f"examples.{arguments.example}")
        clipping: tuple[float, float] = example.clipping
        camera_position: Vector3 = example.camera_position
        camera_fow: float = example.camera_fow
        vertex_buffers: list[list[Vertex]] = example.vertex_buffers
        index_buffers: list[list[int]] = example.index_buffers
        textures: list[Texture] = example.textures
        mesh_positions: list[Vector3] = example.mesh_positions
        mesh_scales: list[Vector3] = example.mesh_scales
        mesh_rotations: list[Vector3] = example.mesh_rotations

        main()

    except KeyboardInterrupt:
        os.system("cls")
