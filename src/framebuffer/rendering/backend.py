import os

from ..linalg import Vector
from ..rendering import Frame

FOREGROUND: str = "\033[38;2;{r};{g};{b}m"
BACKGROUND: str = "\033[48;2;{r};{g};{b}m"
RESET: str = "\033[m"


class Backend:
    def get_size(self) -> tuple[int, int]:
        _terminal_size: os.terminal_size = os.get_terminal_size()

        return _terminal_size.columns, _terminal_size.lines * 2

    def present(self, frame: Frame, /) -> None:
        string_buffer: str = "\033[H"

        for yi in range(0, frame.size[1], 2):
            for xi in range(frame.size[0]):
                upper_pixel: Vector = frame.colour_buffer[yi][xi]
                lower_pixel: Vector = frame.colour_buffer[yi + 1][xi]

                string_buffer += (
                    FOREGROUND.format(r=upper_pixel.x, g=upper_pixel.y, b=upper_pixel.z)
                    + BACKGROUND.format(r=lower_pixel.x, g=lower_pixel.y, b=lower_pixel.z)
                    + "▀"
                )

        print(string_buffer, end=RESET, flush=True)
