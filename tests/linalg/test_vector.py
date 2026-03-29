import random
import unittest

import numpy

from framebuffer.linalg import Vector, Matrix


def rand() -> int:
    return random.randint(-(2**8), 2**8)


class TestVector(unittest.TestCase):
    def setUp(self) -> None:
        self.vector_values: list[float] = list(range(4))
        self.vector: Vector = Vector(self.vector_values)

    def tearDown(self) -> None:
        del self.vector
        del self.vector_values

    def test_init(self) -> None:
        """
        Test initialization of Vector with a list of values.
        """

        self.assertEqual(self.vector._values, self.vector_values)

    def test_zero(self) -> None:
        """
        Test initialization of a zero vector with a specified length.
        """

        for length in range(1, 10):
            vector_values: list[float] = [0] * length
            vector: Vector = Vector(vector_values)

            self.assertEqual(vector._values, vector_values)

    def test_zero_doesnt_support_float_length(self) -> None:
        """
        Test that Vector.zero raises a TypeError when given a noninteger length.
        """

        with self.assertRaises(TypeError):
            Vector.zero(3.5)

    def test_fill(self) -> None:
        """
        Test initialization of a filled vector with a specified length and value.
        """

        for length in range(1, 10):
            fill_value: int = rand()
            vector: Vector = Vector.fill(fill_value, length)

            self.assertEqual(vector._values, [fill_value] * length)

    def test_fill_doesnt_support_float_length(self) -> None:
        """
        Test that Vector.fill raises a TypeError when given a noninteger length.
        """

        with self.assertRaises(TypeError):
            Vector.fill(1.0, 3.5)

    def test_property_getters(self) -> None:
        """
        Test property getters for Vector.
        """
        self.assertEqual(self.vector.x, self.vector_values[0])
        self.assertEqual(self.vector.y, self.vector_values[1])
        self.assertEqual(self.vector.z, self.vector_values[2])
        self.assertEqual(self.vector.w, self.vector_values[3])

        expected_magnitude: float = sum(value**2 for value in self.vector_values) ** 0.5
        self.assertEqual(self.vector.magnitude, expected_magnitude)

        expected_normalised: list[float] = [value / self.vector.magnitude for value in self.vector_values]
        self.assertEqual(self.vector.normalised._values, expected_normalised)

    def test_dot(self) -> None:
        """
        Test that the ``dot`` method correctly computes the dot product of two vectors.
        """

        for _ in range(100):
            random_length: int = random.randint(2, 10)
            vector_a: Vector = Vector([rand() for _ in range(random_length)])
            vector_b: Vector = Vector([rand() for _ in range(random_length)])
            result: float = numpy.dot(vector_a._values, vector_b._values)

            self.assertEqual(vector_a.dot(vector_b), result)

    def test_cross(self) -> None:
        """
        Test that the ``cross`` method correctly computes the cross-product of two vectors.
        """

        vector_a: Vector = Vector([0, 1, 2])
        vector_b: Vector = Vector([3, 4, 5])
        result: list[float] = numpy.cross(vector_a._values, vector_b._values).tolist()

        self.assertEqual(vector_a.cross(vector_b)._values, result)

    def test_len(self) -> None:
        """
        Test that the ``__len__`` method correctly returns the length of the vector.
        """

        for length in range(1, 10):
            vector: Vector = Vector([0.0] * length)

            self.assertEqual(len(vector), length)

    def test_getitem(self) -> None:
        """
        Test that the ``__getitem__`` method correctly retrieves values of the vector.
        """
        self.assertEqual(self.vector[0], self.vector_values[0])
        self.assertEqual(self.vector[1], self.vector_values[1])
        self.assertEqual(self.vector[2], self.vector_values[2])

    def test_iter(self) -> None:
        """
        Test that the ``__iter__`` method correctly iterates over the vector values.
        """

        self.assertEqual(list(self.vector), self.vector_values)

    def test_neg(self) -> None:
        """
        Test that the ``__neg__`` method correctly negates the vector values.
        """

        negated_vector: Vector = -self.vector

        self.assertEqual(negated_vector._values, [-value for value in self.vector_values])

    def test_truediv(self) -> None:
        """
        Test that the ``__truediv__`` method correctly performs true division of the vector by a scalar.
        """

        scalar: float = rand()
        divided_vector: Vector = self.vector / scalar

        self.assertEqual(divided_vector._values, [value / scalar for value in self.vector_values])

    def test_floordiv(self) -> None:
        """
        Test that the ``__floordiv__`` method correctly performs floor division of the vector by a scalar.
        """

        scalar: float = rand()
        floored_vector: Vector = self.vector // scalar

        self.assertEqual(floored_vector._values, [value // scalar for value in self.vector_values])

    def test_mul(self) -> None:
        """
        Test that the ``__mul__`` method correctly performs multiplication of the vector by a scalar.
        """

        scalar: float = rand()
        multiplied_vector: Vector = self.vector * scalar

        self.assertEqual(multiplied_vector._values, [value * scalar for value in self.vector_values])

    def test_add(self) -> None:
        """
        Test that the ``__add__`` method correctly performs addition of the vector with another vector.
        """

        vector_b: Vector = Vector([rand() for _ in range(len(self.vector_values))])
        added_vector: Vector = self.vector + vector_b

        self.assertEqual(
            added_vector._values, [value_a + value_b for value_a, value_b in zip(self.vector_values, vector_b._values)]
        )

    def test_iadd(self) -> None:
        """
        Test that the ``__iadd__`` method correctly performs in-place addition of the vector with another vector.
        """

        vector_a: Vector = Vector([rand() for _ in range(3)])
        vector_a_values: list[float] = vector_a._values[:]
        vector_b: Vector = Vector([rand() for _ in range(3)])
        vector_a += vector_b
        self.assertEqual(
            vector_a._values, [value_a + value_b for value_a, value_b in zip(vector_a_values, vector_b._values)]
        )

    def test_sub(self) -> None:
        """
        Test that the ``__sub__`` method correctly performs subtraction of the vector with another vector.
        """

        vector_b: Vector = Vector([rand() for _ in range(len(self.vector_values))])
        subtracted_vector: Vector = self.vector - vector_b

        self.assertEqual(
            subtracted_vector._values,
            [value_a - value_b for value_a, value_b in zip(self.vector_values, vector_b._values)],
        )

    def test_matmul(self) -> None:
        """
        Test that the ``__matmul__`` method correctly performs matrix multiplication in the vector-matrix case.
        """

        matrix: Matrix = Matrix([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]], shape=(4, 4))
        expected_result: list[float] = numpy.matmul(self.vector._values, matrix._values).tolist()

        self.assertEqual((self.vector @ matrix)._values, expected_result)
