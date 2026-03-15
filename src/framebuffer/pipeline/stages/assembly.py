import itertools

from ..data import Triangle, Vertex


def primitive_assembly(vertex_buffer: list[Vertex], index_buffer: list[int]) -> list[Triangle[Vertex]]:
    return [
        (
            vertex_buffer[indices[0]],
            vertex_buffer[indices[1]],
            vertex_buffer[indices[2]],
        )
        for indices in itertools.batched(index_buffer, n=3)
    ]
