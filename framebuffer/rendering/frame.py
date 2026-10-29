import numpy

from framebuffer.math.linalg import Matrix, Vector, MatrixNDIM


class Frame:
    # TODO [severity 4/5, effort 1/5]: Validate positive dimensions before allocation and aspect calculation.
    def __init__(self, size: Vector[numpy.uint16]) -> None:
        self.size: Vector[numpy.uint16] = size
        width, height = map(int, self.size)
        self.aspect_ratio: float = width / height
        self.color_buffer: MatrixNDIM[numpy.uint8] = numpy.zeros((height, width, 3), dtype=numpy.uint8)
        self.depth_buffer: Matrix[numpy.float64] = numpy.full((height, width), numpy.inf, dtype=numpy.float64)

    def clear(self) -> None:
        self.color_buffer.fill(0)
        self.depth_buffer.fill(numpy.inf)

    def set_size(self, size: Vector[numpy.uint16]) -> None:
        if numpy.array_equal(self.size, size):
            return
        self.size = size
        width, height = map(int, self.size)
        self.aspect_ratio = width / height
        self.color_buffer = numpy.zeros((height, width, 3), dtype=numpy.uint8)
        self.depth_buffer = numpy.full((height, width), numpy.inf, dtype=numpy.float64)
