import math

import numpy
import numpy.linalg


class Vector(object):
    def __init__(self, x=0, y=0, z=0, w=1):
        self._data = numpy.array([x, y, z, w], order="F")

    def set_x(self, x):
        self._data[0] = x

    def get_x(self):
        return self._data[0]

    x = property(get_x, set_x)

    def set_y(self, y):
        self._data[1] = y

    def get_y(self):
        return self._data[1]

    y = property(get_y, set_y)

    def set_z(self, z):
        self._data[2] = z

    def get_z(self):
        return self._data[2]

    z = property(get_z, set_z)

    def set_w(self, w):
        self._data[3] = w

    def get_w(self):
        return self._data[3]

    w = property(get_w, set_w)

    def __str__(self):
        return "<{0}, {1}, {2}, {3}>".format(self.x, self.y, self.z, self.w)

    def raw_data(self):
        return self._data

    def __mul__(self, another):
        if isinstance(another, Vector):
            result = numpy.dot(self._data, another.raw_data())
        elif isinstance(another, Matrix44):
            raw_result = numpy.dot(self._data, another.raw_data())
            result = Vector(
                raw_result[0], raw_result[1], raw_result[2], raw_result[3])
        else:
            raise TypeError("Unsupport type: {0}.".format(type(another)))
        return result

    def __sub__(self, another):
        if isinstance(another, Vector):
            raw_result = numpy.subtract(self._data, another.raw_data())
            result = Vector(
                raw_result[0], raw_result[1], raw_result[2], raw_result[3])
        else:
            raise TypeError("Unsupport type: {0}.".format(type(another)))
        return result

    @classmethod
    def normalize(cls, another):
        sum_ = math.sqrt(another.x**2+another.y**2+another.z**2)
        if sum_ == 0:
            result = cls(0, 0, 0, another.w)
        else:
            result = cls(another.x/sum_, another.y/sum_, another.z/sum_, another.w)
        return result

    @classmethod
    def cross(cls, u, v):
        return cls(
            u.y*v.z-u.z*v.y,
            u.z*v.x-u.x*v.z,
            u.x*v.y-u.y*v.x,
            u.w*v.w)


class Matrix44(object):
    """Row major matrix."""
    def __init__(self, data):
        self._data = numpy.array(data, order="F")

    def get(self, row, column):
        return self._data[row][column]

    def __mul__(self, another):
        if isinstance(another, Matrix44):
            raw_result = numpy.dot(self._data, another.raw_data())
            result = Matrix44(raw_result)
        else:
            raise TypeError("Unsupport type: {0}.".format(type(another)))
        return result

    def __str__(self):
        return (
            "[{0}, {1}, {2}, {3},\n"
            " {4}, {5}, {6}, {7},\n"
            " {8}, {9}, {10}, {11},\n"
            " {12}, {13}, {14}, {15}],").format(
                self._data[0][0],
                self._data[0][1],
                self._data[0][2],
                self._data[0][3],
                self._data[1][0],
                self._data[1][1],
                self._data[1][2],
                self._data[1][3],
                self._data[2][0],
                self._data[2][1],
                self._data[2][2],
                self._data[2][3],
                self._data[3][0],
                self._data[3][1],
                self._data[3][2],
                self._data[3][3])

    def raw_data(self):
        return self._data

    def raw_data_column_major(self):
        return numpy.array(
            [[self._data[0][0], self._data[1][0], self._data[2][0], self._data[3][0]],
            [self._data[0][1], self._data[1][1], self._data[2][1], self._data[3][1]],
            [self._data[0][2], self._data[1][2], self._data[2][2], self._data[3][2]],
            [self._data[0][3], self._data[1][3], self._data[2][3],
             self._data[3][3]]], "F")

    @classmethod
    def translate(cls, x, y, z):
        """Create a translate matrix."""
        return cls([
            (1, 0, 0, 0),
            (0, 1, 0, 0),
            (0, 0, 1, 0),
            (x, y, z, 1)
        ])

    @classmethod
    def look_at_right_hand(cls, eye, target, up):
        zaxis = Vector.normalize(eye-target)
        xaxis = Vector.normalize(Vector.cross(up, zaxis))
        yaxis = Vector.cross(zaxis, xaxis)
        return cls([
            [xaxis.x, yaxis.x, zaxis.x, 0],
            [xaxis.y, yaxis.y, zaxis.y, 0],
            [xaxis.z, yaxis.z, zaxis.z, 0],
            [-(xaxis*eye), -(yaxis*eye), -(zaxis*eye), 1],
        ])

    @classmethod
    def projection_right_hand(cls, fov, aspect, near, far):
        frustum_depth = far-near
        one_over_depth = 1.0/frustum_depth
        return cls([
            [1.0/math.tan(0.5*fov)/aspect, 0, 0, 0],
            [0, 1/math.tan(0.5*fov), 0, 0],
            [0, 0, -far*one_over_depth, -1],
            [0, 0, -2*(far*near)*one_over_depth, 0]
        ])


def main():
    v = Vector(1, 2, 3)
    m = Matrix44.translate(10, 0, 0)
    print v*m
    m2 = Matrix44.translate(0, 10, 0)
    print m*m2
    print m.raw_data_column_major()
    v2 = Vector(3, 2, 1)
    print v2*v
    x = Vector(3, 3, 3, 0)
    print Vector.normalize(x)
    look_at = Matrix44.look_at_right_hand(
        Vector(4, 3, 3),
        Vector(0, 0, 0),
        Vector(0, 1, 0))
    print look_at
    projection = Matrix44.projection_right_hand(
        math.radians(45), 640/480, 0.1, 100.0)
    print projection


if __name__ == "__main__":
    main()
