from __future__ import annotations

from typing import Literal

from .vector4 import Vector4

type _Vector4 = list[float]
type _Matrix4x4 = list[_Vector4]


class Matrix4x4:
    def __init__(self, m: _Matrix4x4) -> None:
        self._m: _Matrix4x4 = m

    @staticmethod
    def zeros() -> Matrix4x4:
        return Matrix4x4(
            [
                [0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0],
            ]
        )

    def take(self, index: Literal[0, 1, 2, 3] = 0, axis: Literal[0, 1] = 0) -> Vector4:
        match axis:
            case 0:
                return Vector4(
                    x=self._m[index][0],
                    y=self._m[index][1],
                    z=self._m[index][2],
                    w=self._m[index][3],
                )

            case 1:
                return Vector4(
                    x=self._m[0][index],
                    y=self._m[1][index],
                    z=self._m[2][index],
                    w=self._m[3][index],
                )

    def __setitem__(self, key: tuple[int, int], value: float) -> None:
        y, x = key
        self._m[y][x] = value

    def __matmul__(self, other: Matrix4x4 | Vector4) -> Matrix4x4 | Vector4:
        # rows
        self_ihat: Vector4 = self.take(index=0, axis=0)
        self_jhat: Vector4 = self.take(index=1, axis=0)
        self_khat: Vector4 = self.take(index=2, axis=0)
        self_ghat: Vector4 = self.take(index=3, axis=0)

        if isinstance(other, Matrix4x4):
            # columns
            other_ihat: Vector4 = other.take(index=0, axis=1)
            other_jhat: Vector4 = other.take(index=1, axis=1)
            other_khat: Vector4 = other.take(index=2, axis=1)
            other_ghat: Vector4 = other.take(index=3, axis=1)

            m00: float = self_ihat.dot(other_ihat)
            m01: float = self_ihat.dot(other_jhat)
            m02: float = self_ihat.dot(other_khat)
            m03: float = self_ihat.dot(other_ghat)
            m10: float = self_jhat.dot(other_ihat)
            m11: float = self_jhat.dot(other_jhat)
            m12: float = self_jhat.dot(other_khat)
            m13: float = self_jhat.dot(other_ghat)
            m20: float = self_khat.dot(other_ihat)
            m21: float = self_khat.dot(other_jhat)
            m22: float = self_khat.dot(other_khat)
            m23: float = self_khat.dot(other_ghat)
            m30: float = self_ghat.dot(other_ihat)
            m31: float = self_ghat.dot(other_jhat)
            m32: float = self_ghat.dot(other_khat)
            m33: float = self_ghat.dot(other_ghat)

            return Matrix4x4(
                [
                    [m00, m01, m02, m03],
                    [m10, m11, m12, m13],
                    [m20, m21, m22, m23],
                    [m30, m31, m32, m33],
                ]
            )

        elif isinstance(other, Vector4):
            return Vector4(
                x=self_ihat.dot(other),
                y=self_jhat.dot(other),
                z=self_khat.dot(other),
                w=self_ghat.dot(other),
            )

        else:
            raise NotImplementedError
