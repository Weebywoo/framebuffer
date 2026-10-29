import numpy

from .base_component import BaseComponent
from framebuffer.scene.transform import Transform
from framebuffer.platform.windows import WindowsInterface, RegisteredKey


class KeyboardControlComponent(BaseComponent):
    def __init__(self, factor: float) -> None:
        self.factor: float = factor

    # TODO [severity 2/5, effort 1/5]: Update position scalars without temporary direction arrays.
    def apply(self, transform: Transform, elapsed_time: float, dt: float) -> None:
        if not WindowsInterface.get_game_is_active_window():
            return

        key_presses: dict[RegisteredKey, bool] = WindowsInterface.get_key_update()

        if key_presses["w"]:
            transform.position += numpy.array([0, 0, 1]) * self.factor

        if key_presses["a"]:
            transform.position += numpy.array([-1, 0, 0]) * self.factor

        if key_presses["s"]:
            transform.position += numpy.array([0, 0, -1]) * self.factor

        if key_presses["d"]:
            transform.position += numpy.array([1, 0, 0]) * self.factor
