import os

import numpy

from framebuffer.math.linalg import Vector
from framebuffer.rendering.frame import Frame


class Backend:
    FOREGROUND: str = "\033[38;2;{r};{g};{b}m"
    BACKGROUND: str = "\033[48;2;{r};{g};{b}m"

    @staticmethod
    # TODO [severity 1/5, effort 2/5]: Cache terminal size if polling becomes costly.
    def get_size() -> Vector[numpy.uint16]:
        _terminal_size: os.terminal_size = os.get_terminal_size()

        return numpy.array([_terminal_size.columns, _terminal_size.lines * 2], dtype=numpy.uint16)

    # TODO [severity 4/5, effort 4/5]: Emit only changed terminal regions.
    # TODO [severity 4/5, effort 3/5]: Reuse active ANSI colors.
    @classmethod
    def present(cls, frame: Frame) -> None:
        string_buffer: list[str] = ["\033[H"]

        for yi in range(0, frame.size[1], 2):
            for xi in range(frame.size[0]):
                upper_pixel: Vector[numpy.uint8] = frame.color_buffer[yi][xi]
                lower_pixel: Vector[numpy.uint8] = frame.color_buffer[yi + 1][xi]

                string_buffer.append(
                    f"\033[38;2;{upper_pixel[0]};{upper_pixel[1]};{upper_pixel[2]}m"
                    f"\033[48;2;{lower_pixel[0]};{lower_pixel[1]};{lower_pixel[2]}m"
                    "▀"
                )

        print("".join(string_buffer) + "\033[m", flush=True, end="")
