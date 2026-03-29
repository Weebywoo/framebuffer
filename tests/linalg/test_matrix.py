import itertools
import random
import unittest

import numpy

from framebuffer.linalg import Matrix, Vector


def rand() -> float:
    return random.randint(-(2**8), 2**8)


class TestMatrix(unittest.TestCase):
    def setUp(self) -> None:
        self.matrix_values: list[list[float]] = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
        self.matrix: Matrix = Matrix(self.matrix_values, shape=(3, 3))

    def tearDown(self) -> None:
        del self.matrix
        del self.matrix_values

    def test_init(self) -> None:
        """
        Test initialization of Matrix with a list of values.
        """

        self.assertEqual(self.matrix._values, self.matrix_values)

    def test_transpose(self) -> None:
        """
        Tests that the transpose of the matrix is correct.
        """

        self.assertEqual(self.matrix.transpose._values, [[0, 3, 6], [1, 4, 7], [2, 5, 8]])

    def test_zeros(self) -> None:
        """
        Test initialization of a zero matrix with a specified shape.
        """

        for shape in itertools.product(range(2, 5), repeat=2):
            zeros_values: list[list[float]] = [[0] * shape[1] for _ in range(shape[0])]

            self.assertEqual(Matrix.zeros(shape)._values, zeros_values)

    def test_shape(self) -> None:
        """
        Test that the ``shape`` property returns the correct dimensions of the matrix.
        """

        self.assertEqual(self.matrix.shape, (3, 3))

    def test_take(self) -> None:
        """
        Test that the ``take()`` method returns the correct Vector.
        """

        for row_index in range(self.matrix.shape[0]):
            expected_vector: Vector = Vector(self.matrix_values[row_index])

            self.assertEqual(self.matrix.take(row_index, axis=0)._values, expected_vector._values)

        for column_index in range(self.matrix.shape[1]):
            expected_vector: Vector = Vector(
                [
                    self.matrix_values[0][column_index],
                    self.matrix_values[1][column_index],
                    self.matrix_values[2][column_index],
                ]
            )

            self.assertEqual(self.matrix.take(column_index, axis=1)._values, expected_vector._values)

    def test_setitem_getitem(self) -> None:
        """
        Test that the ``__setitem__`` and ``__getitem__`` methods correctly set and retrieve values in the matrix.
        """

        for row_index, column_index in itertools.product(range(self.matrix.shape[1]), range(self.matrix.shape[0])):
            self.matrix[row_index, column_index] = 100
            self.assertEqual(self.matrix[row_index, column_index], 100)

    def test_matmul_matrix_matrix(self) -> None:
        """
        Test that the ``__matmul__`` method correctly computes matrix @ matrix multiplication values.
        """

        for shape in itertools.product(range(2, 10), range(2, 10)):
            shape_a: tuple[int, int] = (shape[0], shape[1])
            shape_b: tuple[int, int] = (shape[1], shape[0])
            matrix_a: Matrix = Matrix([[rand()] * shape_a[0] for _ in range(shape_a[1])], shape=shape_a)
            matrix_b: Matrix = Matrix([[rand()] * shape_b[0] for _ in range(shape_b[1])], shape=shape_b)
            result: list[list[float]] = numpy.matmul(matrix_a._values, matrix_b._values).tolist()

            self.assertEqual((matrix_a @ matrix_b)._values, result)
