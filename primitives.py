import numpy as np


class PhysicalObject(object):
    def __init__(self, position, colour):
        self.pos = np.asarray(position)
        self.colour = np.asarray(colour)

    def intersect(self, ray):
        raise NotImplementedError

    def get_normal_with(self, point):
        raise NotImplementedError


class Vector(object):
    def __init__(self, direction):
        self.direction = np.asarray(direction)

    def length(self):
        return np.linalg.norm(self.direction)

    def normalized(self):
        return Vector(self.direction / self.length())


class Ray(Vector):
    def __init__(self, origin, *args, **kwargs):
        super(Ray, self).__init__(*args, **kwargs)
        self.origin = origin

    def at(self, s):
        return self.origin + s * self.direction


class Light(PhysicalObject):
    pass


class Sphere(PhysicalObject):
    def __init__(self, radius, *args, **kwargs):
        super(Sphere, self).__init__(*args, **kwargs)
        self.radius = radius

    def intersect(self, ray, return_dist=False):
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
        if return_dist:
            dist_intersect = s * ray.length()
            return dist_intersect
        else:
            return s

    def get_normal_with(self, point):
        vec_pt_centre = Vector(point - self.pos)
        return vec_pt_centre.normalized()


class Cube(PhysicalObject):
    def __init__(self, length, *args, **kwargs):
        super(Cube, self).__init__(*args, **kwargs)
        self.length = length


class Cylinder(PhysicalObject):
    def __init__(self, radius, height, *args, **kwargs):
        super(Cylinder, self).__init__(*args, **kwargs)
        self.radius = radius
        self.height = height
