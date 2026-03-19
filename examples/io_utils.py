from typing import Any

from framebuffer.linalg import Vector
from framebuffer.pipeline.data import Vertex


def write_bmp(path: str, data: list[list[Any]]) -> None:
    # Each row in the Pixel array is padded to a multiple of 4 bytes in size
    image_data: list[bytes] = []

    for line in data:
        image_data_line: list[bytes] = []

        for pixel in line:
            image_data_line.append(int(pixel.z).to_bytes())
            image_data_line.append(int(pixel.y).to_bytes())
            image_data_line.append(int(pixel.x).to_bytes())

        if (missing_padding := len(image_data_line) % 4) != 0:
            image_data_line.append(bytes(missing_padding))

        image_data.extend(image_data_line)

    BITMAP_FILE_HEADER: dict[str, bytes] = {
        "bf_type": b"\x42\x4d",
        "bf_size": (14 + 40 + len(image_data)).to_bytes(4, "little"),
        "bf_reserved": b"\x00\x00\x00\x00",
        "bf_off_bits": b"\x36\x00\x00\x00",
    }
    BITMAP_INFO_HEADER: dict[str, bytes] = {
        "bi_size": b"\x28\x00\x00\x00",
        "bi_width": len(data[0]).to_bytes(4, "little"),
        "bi_height": (2**32 - len(data)).to_bytes(4, "little"),
        "bi_planes": b"\x01\x00",
        "bi_bit_count": b"\x18\x00",
        "bi_compression": b"\x00\x00\x00\x00",
        "bi_size_image": len(image_data).to_bytes(4, "little"),
        "bi_x_pels_per_meter": b"\x00\x00\x00\x00",
        "bi_y_pels_per_meter": b"\x00\x00\x00\x00",
        "bi_clr_used": b"\x00\x00\x00\x00",
        "bi_clr_important": b"\x00\x00\x00\x00",
    }

    with open(path, "wb") as io_wrapper:
        io_wrapper.write(b"".join(list(BITMAP_FILE_HEADER.values()) + list(BITMAP_INFO_HEADER.values()) + image_data))


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


def handle_uvs(uvs: list[Vector], uv_indices: list[int]) -> list[Vector]:
    triangle_uvs: list[Vector] = []

    for index in uv_indices:
        uv: Vector = uvs[index]
        triangle_uvs.append(Vector([uv.x, 1.0 - uv.y]))

    return triangle_uvs


def load_obj(filepath: str) -> tuple[list[Vertex], list[int]]:
    positions: list[Vector] = []
    uvs: list[Vector] = []
    normals: list[Vector] = []

    vertices: list[Vertex] = []
    indices: list[int] = []

    with open(filepath) as file:
        obj_file: list[str] = file.readlines()

    for line in obj_file:
        line_args: list[str] = line.split()

        match line_args[0]:
            case "v":
                positions.append(
                    Vector([float(line_args[1:][0]), float(line_args[1:][1]), float(line_args[1:][2]), 1.0])
                )

            case "vn":
                normals.append(
                    Vector(
                        [
                            float(line_args[1:][0]),
                            float(line_args[1:][1]),
                            float(line_args[1:][2]),
                        ]
                    )
                )

            case "vt":
                uvs.append(
                    Vector(
                        [
                            float(line_args[1:][0]),
                            float(line_args[1:][1]),
                        ]
                    )
                )

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
