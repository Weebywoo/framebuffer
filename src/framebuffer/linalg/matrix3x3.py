from __future__ import annotations

from typing import Literal

from .vector3 import Vector3

type _Vector3 = list[float]
type _Matrix3x3 = list[_Vector3]


class Matrix3x3:
    def __init__(self, m: _Matrix3x3) -> None:
        self._m: _Matrix3x3 = m

    def take(self, index: Literal[0, 1, 2] = 0, axis: Literal[0, 1] = 0) -> Vector3:
        match axis:
            case 0:
                return Vector3(
                    x=self._m[index][0],
                    y=self._m[index][1],
                    z=self._m[index][2],
                )

            case 1:
                return Vector3(
                    x=self._m[0][index],
                    y=self._m[1][index],
                    z=self._m[2][index],
                )

    def __matmul__(self, other: Matrix3x3 | Vector3) -> Matrix3x3 | Vector3:
        # rows
        self_ihat: Vector3 = self.take(index=0, axis=0)
        self_jhat: Vector3 = self.take(index=1, axis=0)
        self_khat: Vector3 = self.take(index=2, axis=0)

        if isinstance(other, Matrix3x3):
            # columns
            other_ihat: Vector3 = other.take(index=0, axis=1)
            other_jhat: Vector3 = other.take(index=1, axis=1)
            other_khat: Vector3 = other.take(index=2, axis=1)

            m00: float = self_ihat.dot(other_ihat)
            m01: float = self_ihat.dot(other_jhat)
            m02: float = self_ihat.dot(other_khat)
            m10: float = self_jhat.dot(other_ihat)
            m11: float = self_jhat.dot(other_jhat)
            m12: float = self_jhat.dot(other_khat)
            m20: float = self_khat.dot(other_ihat)
            m21: float = self_khat.dot(other_jhat)
            m22: float = self_khat.dot(other_khat)

            return Matrix3x3(
                [
                    [m00, m01, m02],
                    [m10, m11, m12],
                    [m20, m21, m22],
                ]
            )

        elif isinstance(other, Vector3):
            return Vector3(
                x=self_ihat.dot(other),
                y=self_jhat.dot(other),
                z=self_khat.dot(other),
            )

        else:
            raise NotImplementedError
