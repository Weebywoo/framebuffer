import math

from ..linalg import Vector2, Vector4

type ColourBuffer = list[list[Vector4]]
type DepthBuffer = list[list[float]]


class Frame:
    def __init__(self, size: tuple[int, int]) -> None:
        self.size: tuple[int, int] = size
        self.aspect_ratio: float = self.size[0] / self.size[1]
        self.colour_buffer: ColourBuffer = [[Vector4.zeros(dtype=int)] * self.size[0] for _ in range(self.size[1])]
        self.depth_buffer: DepthBuffer = [[math.inf] * self.size[0] for _ in range(self.size[1])]

    def clear(self) -> None:
        for yi in range(self.size[1]):
            for xi in range(self.size[0]):
                self.colour_buffer[yi][xi] = Vector4.zeros(dtype=int)
                self.depth_buffer[yi][xi] = math.inf

    def set_size(self, size: tuple[int, int]) -> None:
        self.size = size
        self.colour_buffer = [[Vector4.zeros(dtype=int)] * self.size[0] for _ in range(self.size[1])]
        self.depth_buffer = [[math.inf] * self.size[0] for _ in range(self.size[1])]

    def draw_pixel(self, position: "Vector2", colour: Vector4, depth: float) -> None:
        x: int = int(position.x)
        y: int = int(position.y)
        self.colour_buffer[y][x] = colour
        self.depth_buffer[y][x] = depth

    def compare_depth(self, position: "Vector2", depth: float) -> bool:
        x: int = int(position.x)
        y: int = int(position.y)

        return depth < self.depth_buffer[y][x]
