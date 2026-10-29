import json
from pathlib import Path

import numpy

from framebuffer.math.linalg import Vector
from framebuffer.pipeline.data.vertex import Vertex

type VertexBuffer = list[Vertex]
type IndexBuffer = list[int]
type Scene = tuple[VertexBuffer, IndexBuffer]
type SceneList = list[Scene]


# TODO [severity 3/5, effort 3/5]: Support polygon faces, missing attributes, and negative indices.
def handle_f(data: list[str]) -> tuple[list[tuple[int, int, int]], ...]:
    i_clump_0: list[str] = data[0].split("/")
    i_clump_1: list[str] = data[1].split("/")
    i_clump_2: list[str] = data[2].split("/")
    i_clump_3: list[str] | None = data[3].split("/") if len(data) == 4 else None

    def separate_data(index: int) -> list[tuple[int, int, int]]:
        indices: list[tuple[int, int, int]] = []
        i_0: int = int(i_clump_0[index]) - 1
        i_1: int = int(i_clump_1[index]) - 1
        i_2: int = int(i_clump_2[index]) - 1

        if i_clump_3:
            i_3: int = int(i_clump_3[index]) - 1

            indices.append((i_0, i_1, i_2))
            indices.append((i_0, i_2, i_3))

        else:
            indices.append((i_0, i_1, i_2))

        return indices

    face_indices: list[tuple[int, int, int]] = separate_data(0)
    texture_indices: list[tuple[int, int, int]] = separate_data(1)
    normal_indices: list[tuple[int, int, int]] = separate_data(2)

    return face_indices, texture_indices, normal_indices


class MeshLoader:
    @classmethod
    def load(cls, filepath: str, /) -> tuple[list[Vertex], list[int]]:
        match Path(filepath).suffix.lower():
            case ".obj":
                return cls.load_obj(filepath)

        raise ValueError(f"Unsupported file format: {filepath}")

    @staticmethod
    # TODO [severity 3/5, effort 3/5]: Reuse vertices with identical position, UV, and normal indices.
    def load_obj(filepath: str) -> Scene:
        positions: list[Vector[numpy.float64]] = []
        uvs: list[Vector[numpy.float64]] = []
        normals: list[Vector[numpy.float64]] = []
        vertices: list[Vertex] = []
        indices: list[int] = []

        with open(filepath) as file:
            obj_file: list[str] = file.readlines()

        for line in obj_file:
            line_args: list[str] = line.split()
            if not line_args or line_args[0].startswith("#"):
                continue

            match line_args[0]:
                case "v":
                    position: Vector[numpy.float64] = numpy.array(
                        [
                            float(line_args[1:][0]),
                            float(line_args[1:][1]),
                            float(line_args[1:][2]),
                            1.0,
                        ]
                    )

                    positions.append(position)

                case "vn":
                    normal: Vector[numpy.float64] = numpy.array(
                        [
                            float(line_args[1:][0]),
                            float(line_args[1:][1]),
                            float(line_args[1:][2]),
                        ]
                    )
                    normals.append(normal)

                case "vt":
                    uv: Vector[numpy.float64] = numpy.array(
                        [
                            float(line_args[1:][0]),
                            float(line_args[1:][1]),
                        ]
                    )

                    uvs.append(uv)

                case "f":
                    for vertex_indices, uv_indices, normal_indices in zip(*handle_f(line_args[1:])):
                        for vertex_index, uv_index, normal_index in zip(vertex_indices, uv_indices, normal_indices):
                            vertices.append(
                                Vertex(
                                    position=positions[vertex_index],
                                    normal=normals[normal_index],
                                    uv=uvs[uv_index],
                                )
                            )
                            indices.append(len(vertices) - 1)

        return vertices, indices

    @classmethod
    # TODO [severity 3/5, effort 4/5]: Return mesh buffers or explicitly reject unsupported GLB loading.
    def load_glb(cls, filepath: str) -> None:
        raise NotImplementedError

        with open(filepath, "rb") as file:
            glb_data: bytes = file.read()

        magic_identifier: bytes = glb_data[:4]
        format_version: int = int.from_bytes(glb_data[4:8], "little")

        if magic_identifier != b"glTF":
            raise ValueError("Invalid GLB magic identifier")

        if format_version != 2:
            raise ValueError("Unsupported GLB format version")

        chunk_index: int = 12
        chunk_length: int = int.from_bytes(glb_data[chunk_index : chunk_index + 4], "little")
        chunk_type: bytes = glb_data[chunk_index + 4 : chunk_index + 8]
        chunk_data: bytes = glb_data[chunk_index + 8 : chunk_index + 8 + chunk_length]
        chunk_index += chunk_length

        if chunk_type != b"JSON":
            raise ValueError("First GLB chunk must be a JSON chunk")

        json_data: dict[str, str] = json.loads(chunk_data.decode("utf-8"))

        print(json.dumps(json_data, indent=4))
