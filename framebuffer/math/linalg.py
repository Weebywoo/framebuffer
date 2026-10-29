import math

import numba
import numpy

type Vector[T: numpy.generic] = numpy.ndarray[tuple[int], numpy.dtype[T]]
type Matrix[T: numpy.generic] = numpy.ndarray[tuple[int, int], numpy.dtype[T]]
type MatrixNDIM[T: numpy.generic] = numpy.ndarray[tuple[int, ...], numpy.dtype[T]]


@numba.jit(nopython=True)
# TODO [severity 4/5, effort 3/5]: Precompute triangle edge coefficients.
def signed_triangle_area(a: Vector[numpy.float64], b: Vector[numpy.float64], c: Vector[numpy.float64]) -> numpy.float64:
    return ((c[0] - a[0]) * (b[1] - a[1]) - (c[1] - a[1]) * (b[0] - a[0])) * 0.5


@numba.jit(nopython=True)
# TODO [severity 5/5, effort 3/5]: Replace area arrays with incremental edge tests.
def point_in_triangle(
    position_0: Vector[numpy.float64],
    position_1: Vector[numpy.float64],
    position_2: Vector[numpy.float64],
    point: Vector[numpy.uint16],
) -> Vector[numpy.float64]:
    area_abp: numpy.float64 = signed_triangle_area(position_0, position_1, point.astype(numpy.float64))
    area_bcp: numpy.float64 = signed_triangle_area(position_1, position_2, point.astype(numpy.float64))
    area_cap: numpy.float64 = signed_triangle_area(position_2, position_0, point.astype(numpy.float64))
    has_pos: bool = area_abp > 0 or area_bcp > 0 or area_cap > 0
    has_neg: bool = area_abp < 0 or area_bcp < 0 or area_cap < 0
    in_triangle: float = not (has_pos and has_neg) and area_abp + area_bcp + area_cap != 0.0

    return numpy.array([in_triangle, area_abp, area_bcp, area_cap])


@numba.jit(nopython=True)
def calc_2d_aabb(
    position_0: Vector[numpy.float64],
    position_1: Vector[numpy.float64],
    position_2: Vector[numpy.float64],
    dimensions: Vector[numpy.uint16],
) -> tuple[int, int, int, int]:
    width, height = int(dimensions[0]), int(dimensions[1])
    min_x: float = min(position_0[0], position_1[0], position_2[0])
    min_y: float = min(position_0[1], position_1[1], position_2[1])
    max_x: float = max(position_0[0], position_1[0], position_2[0])
    max_y: float = max(position_0[1], position_1[1], position_2[1])
    bounding_box_start_x = max(0, math.ceil(min_x))
    bounding_box_start_y = max(0, math.ceil(min_y))
    bounding_box_end_x = min(math.floor(max_x), width - 1)
    bounding_box_end_y = min(math.floor(max_y), height - 1)

    return bounding_box_start_x, bounding_box_start_y, bounding_box_end_x, bounding_box_end_y


@numba.jit(nopython=True)
def lerp(a: Vector[numpy.float64], b: Vector[numpy.float64], t: numpy.float64) -> Vector[numpy.float64]:
    return a * (1 - t) + b * t
