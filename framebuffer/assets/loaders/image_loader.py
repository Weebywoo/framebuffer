import numpy
from PIL import Image

from framebuffer.math.linalg import MatrixNDIM


class ImageLoader:
    @classmethod
    def load(cls, filepath: str) -> MatrixNDIM[numpy.uint8]:
        with Image.open(filepath) as image:
            return numpy.array(image.convert("RGB"), dtype=numpy.uint8)
