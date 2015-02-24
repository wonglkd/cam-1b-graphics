import numpy as np


class PhysicalObject(object):
    def __init__(self, position, colour):
        self.pos = np.asarray(position)
        self.colour = np.asarray(colour)

    def intersect(self, ray):
        raise NotImplementedError


class Vector(object):
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction

    def length(self):
        return np.linalg.norm(self.direction)


class Ray(Vector):
    pass


class Light(PhysicalObject):
    def __init__(self, *args, **kwargs):
        super(Light, self).__init__(*args, **kwargs)


class Sphere(PhysicalObject):
    def __init__(self, radius, *args, **kwargs):
        super(Sphere, self).__init__(*args, **kwargs)
        self.radius = radius

    def intersect(self, ray):
        """
        Intersection math.
        P = O + sD, s >= 0
        (P - C)^2 = r^2     distance from point to centre = r
        (O + sD - C)^2 = r^2
        (O-C + sD) ^2 = r^2
        (O-C)^2 + (O-C)(D)(2) * s + D^2 * s^2 = r^2
        D^2 * s^2 + 2(O-C)(D) * s + [(O-C)^2 - r^2] = 0

        a = D^2
        b = 2(O-C)(D)
        c = (O-C)^2 - r^2
        """
        a = ray.direction.dot(ray.direction)
        b = 2. * ray.direction.dot(ray.origin - self.pos)
        o_minus_c = ray.origin - self.pos
        c = o_minus_c.dot(o_minus_c) - pow(self.radius, 2)
        d = pow(b, 2) - 4 * a * c
        if d < 0:
            return np.inf
        d = np.sqrt(d)
        s = min((-b + d) / (2 * a), (-b - d) / (2 * a))
        dist_intersect = s * ray.length()
        return dist_intersect


class Cube(PhysicalObject):
    def __init__(self, length, *args, **kwargs):
        super(Cube, self).__init__(*args, **kwargs)
        self.length = length


class Cylinder(PhysicalObject):
    def __init__(self, radius, height, *args, **kwargs):
        super(Cylinder, self).__init__(*args, **kwargs)
        self.radius = radius
        self.height = height
