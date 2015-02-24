from primitives import Sphere
from primitives import Cube
from primitives import Cylinder
from primitives import Light
import screen


class RayTracer(object):
    def set_scene(self, scene):
        self.scene = scene

    def trace_ray(self, ray):
        # for every object in the scene
        for obj in self.scene:
            if obj.intersect(ray):
                # if intersection point is closest so far to the eye, save it
                pass
        # return colour of object at closest intersection point


def main():
    rt = RayTracer()

    # 1. Form a scene
    scene = [Sphere(radius=1., position=(0, 0, 0)),
             Sphere(radius=2., position=(4, 5, 0))]
    rt.set_scene(scene)

    # 2. Model sources of illumination
    rt.light_sources = [Light(position=(0, 0, 10), colour=(1, 1, 1))]
    rt.light_ambient = 0.05

    # 3. Trace a ray to find its intersection with the nearest surface
    # Select eye point and screen plane

    # for every pixel in the screen plane
    for x in xrange(screen.canvas_width):
        for y in xrange(screen.canvas_height):
            # determine the ray from the eye through the pixel's centre
            rt.trace_ray(1)

            # TODO: super-sampling

    # 4. Trace ray from intersection to the sources of illumination
    # 5. (Optional) reflection, transparency, refraction
    # 6. Display results on a grid of pixels

if __name__ == '__main__':
    main()
