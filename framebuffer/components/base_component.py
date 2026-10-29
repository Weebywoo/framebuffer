from typing import Protocol

from framebuffer.scene.transform import Transform


class BaseComponent(Protocol):
    def apply(self, transform: Transform, elapsed_time: float, dt: float) -> None:
        pass
