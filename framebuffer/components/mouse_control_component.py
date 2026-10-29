from framebuffer.math.linalg import Vector

from .base_component import BaseComponent
from framebuffer.scene.transform import Transform
from framebuffer.platform.windows import WindowsInterface
import numpy


# TODO [severity 3/5, effort 2/5]: Recenter the mouse within the active window.
class MouseControlComponent(BaseComponent):
    def __init__(self, sensitivity: float) -> None:
        self.sensitivity: float = sensitivity

    def apply(self, transform: Transform, elapsed_time: float, dt: float) -> None:
        if not WindowsInterface.get_game_is_active_window():
            return

        mouse_position: Vector[numpy.float64] = WindowsInterface.get_mouse_update()
        mouse_position[1] *= -1
        transform.rotation += numpy.array(list(reversed(mouse_position)) + [0.0]) * self.sensitivity
