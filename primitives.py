class PhysicalObject(object):
    def __init__(self, position):
        self.pos = position

    def intersect(self, ray):
        raise NotImplementedError


class Vector(object):
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction


class Ray(Vector):
    pass


class Light(PhysicalObject):
    def __init__(self, colour, *args, **kwargs):
        super(Light, self).__init__(*args, **kwargs)
        self.colour = colour


class Sphere(PhysicalObject):
    def __init__(self, radius, *args, **kwargs):
        super(Sphere, self).__init__(*args, **kwargs)
        self.radius = radius


class Cube(PhysicalObject):
    def __init__(self, length, *args, **kwargs):
        super(Cube, self).__init__(*args, **kwargs)
        self.length = length


class Cylinder(PhysicalObject):
    def __init__(self, radius, height, *args, **kwargs):
        super(Cylinder, self).__init__(*args, **kwargs)
        self.radius = radius
        self.height = height
