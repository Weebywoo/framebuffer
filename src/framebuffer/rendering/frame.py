import math

from ..linalg import Vector

type ColourBuffer = list[list[Vector]]
type DepthBuffer = list[list[float]]


class Frame:
    def __init__(self, size: tuple[int, int]) -> None:
        self.size: tuple[int, int] = size
        self.aspect_ratio: float = self.size[0] / self.size[1]
        self.colour_buffer: ColourBuffer = [[Vector.zero(4).astype(int)] * self.size[0] for _ in range(self.size[1])]
        self.depth_buffer: DepthBuffer = [[math.inf] * self.size[0] for _ in range(self.size[1])]

    def clear(self) -> None:
        for yi in range(self.size[1]):
            for xi in range(self.size[0]):
                self.colour_buffer[yi][xi] = Vector.zero(4).astype(int)
                self.depth_buffer[yi][xi] = math.inf

    def set_size(self, size: tuple[int, int]) -> None:
        self.size = size
        self.colour_buffer = [[Vector.zero(4).astype(int)] * self.size[0] for _ in range(self.size[1])]
        self.depth_buffer = [[math.inf] * self.size[0] for _ in range(self.size[1])]

    def draw_pixel(self, position: Vector, colour: Vector, depth: float) -> None:
        x: int = position.x
        y: int = position.y
        self.colour_buffer[y][x] = colour
        self.depth_buffer[y][x] = depth

    def compare_depth(self, position: Vector, depth: float) -> bool:
        x: int = position.x
        y: int = position.y

        return depth < self.depth_buffer[y][x]
