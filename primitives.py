import numpy as np


def normalize(vector):
    return np.linalg.norm(vector)


class PhysicalObject(object):
    def __init__(self, position, colour):
        self.pos = np.asarray(position)
        self.colour = np.asarray(colour)
        self.coef_specular = 1.
        self.coef_diffuse = 1.

    def intersect(self, ray):
        raise NotImplementedError

    def get_normal_with(self, point):
        raise NotImplementedError


class Vector(object):
    def __init__(self, direction):
        self.direction = np.asarray(direction)
        self.dir = self.direction

    def length(self):
        return normalize(self.direction)

    def normalized(self):
        """ N.B. This modifies the current object. """
        self.direction /= self.length()
        return self

    def __repr__(self):
        return 'Vector(direction={}'.format(self.direction)


class Ray(Vector):
    def __init__(self, origin, *args, **kwargs):
        if 'towards' in kwargs:
            kwargs['direction'] = kwargs.pop('towards') - origin
        super(Ray, self).__init__(*args, **kwargs)
        self.origin = origin

    def at(self, s):
        return self.origin + s * self.direction

    def __repr__(self):
        return 'Ray(origin={}, direction={}'.format(self.origin, self.direction)


class Light(PhysicalObject):
    pass


def solve(a, b, c):
    """ Solve a quadratic equation. """
    d = pow(b, 2) - 4 * a * c
    if d < 0:
        return [np.inf]
    d = np.sqrt(d)
    return [(-b + d) / (2 * a), (-b - d) / (2 * a)]


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
        return min(solve(a, b, c))

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

    def intersect(self, ray):
        """ open cylinder. TODO: lids. """
        dir_xz = ray.dir[[0, 2]]
        origin_xz = ray.origin[[0, 2]]
        pos_xz = self.pos[[0, 2]]
        a = (dir_xz ** 2).sum()
        b = dir_xz.dot(origin_xz - pos_xz) * 2
        c = ((origin_xz - pos_xz) ** 2).sum() - self.radius ** 2
        in_bounds = lambda y: (self.pos[1] - self.height/2. <= y
                               and y <= self.pos[1] + self.height/2.)
        sols = [s for s in solve(a, b, c) if s > 0 and in_bounds(ray.at(s)[1])]
        return min(sols + [np.inf])

    def get_normal_with(self, point):
        vec_pt_centre = Vector(point - self.pos)
        vec_pt_centre.direction[1] = 0.
        return vec_pt_centre.normalized()
