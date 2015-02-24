from primitives import Sphere
from primitives import Cube
from primitives import Cylinder
from primitives import Light
from primitives import Ray
from primitives import Vector
import screen_col as screen
import numpy as np


class RayTracer(object):
    def __init__(self):
        # for specular  reflection
        self.n_roughness = 10

    def set_scene(self, scene):
        self.scene = scene

    def trace_ray(self, ray):
        s_closest_intersection = np.inf
        closest_obj = None

        """ Find closest intersection point to eye """
        for obj in self.scene:
            s_intersect = obj.intersect(ray)
            # if intersection point is closest so far to the eye, save it
            if s_intersect < s_closest_intersection:
                s_closest_intersection = s_intersect
                closest_obj = obj

        if closest_obj is None:
            return

        """ Shading: return colour of object at closest intersection point """
        # Solid colour as a stopgap
        # return closest_obj.colour

        # calculate normal to object at intersection point
        intersection_pt = ray.at(s_closest_intersection)
        norm_at_intersect = closest_obj.get_normal_with(intersection_pt)

        colour = np.zeros(3)

        # shoot rays from point to light sources
        for light in self.light_sources:
            ray_intersect_light = Ray(origin=intersection_pt,
                                      towards=light.pos).normalized()
            v_i = ray_intersect_light.direction
            v_n = norm_at_intersect.direction
            """ calculate diffuse reflections off objects at that point """
            intensity_diffuse = v_n.dot(v_i)
            intensity_diffuse = max(intensity_diffuse, 0.)
            intensity_diffuse *= closest_obj.coef_diffuse
            colour += intensity_diffuse * closest_obj.colour

            """ calculate specular reflections off objects at that point """
            # TODO: specular reflection seems buggy
            v_reflected = -v_i - 2 * -v_i.dot(v_n) * v_n
            v_viewer = Vector(self.pt_eye - intersection_pt).normalized().direction
            intensity_specular = max(v_reflected.dot(v_viewer), 0.)
            # print intensity_specular
            intensity_specular = pow(intensity_specular, self.n_roughness)
            intensity_specular *= closest_obj.coef_specular
            colour += intensity_specular * closest_obj.colour

        """ that + ambient illumination gives colour of object """
        colour += self.light_ambient

        return colour


def main():
    rt = RayTracer()

    # 1. Form a scene
    scene = []
    # scene.append(Sphere(radius=1., position=(0, 0, 0)))
    # scene.append(Sphere(radius=2., position=(4, 5, 0)))
    scene.append(Sphere(radius=2., position=[-1.5, 0., 5], colour=[1, 0, 0]))
    scene.append(Sphere(radius=2., position=[1.5, 0., 6], colour=[0, 1, 0]))
    rt.set_scene(scene)

    # 2. Model sources of illumination
    # rt.light_sources = [Light(position=(1, 0, 0), colour=(1., 1., 1.))]
    rt.light_sources = [Light(position=(-1, 0, 2), colour=(1., 1., 1.))]
    rt.light_ambient = 0.02 * np.ones(3)

    # 3. Trace a ray to find its intersection with the nearest surface
    # Select eye point and screen plane
    rt.pt_eye = np.array([0., 0., -1.])
    # x_0, y_0, x_1, y_1
    plane_screen = [-1., -1., 1., 1.]
    pts_x = np.linspace(plane_screen[0], plane_screen[2], screen.canvas_width)
    pts_y = np.linspace(plane_screen[1], plane_screen[3], screen.canvas_height)

    # for every pixel in the screen plane
    for i, x in enumerate(pts_x):
        for j, y in enumerate(pts_y):
            pt_on_screen = np.array([x, y, 0.])
            pt_colour = np.zeros(3)

            # determine the ray from the eye through the pixel's centre

            # to make extension easier e.g. for supersampling
            pt_origin = rt.pt_eye

            ray_eye_to_pixel = Ray(origin=pt_origin,
                                   towards=pt_on_screen)

            # 4. Trace ray from intersection to the sources of illumination
            # 5. (Optional) reflection, transparency, refraction
            # TODO: super-sampling
            rt_colour = rt.trace_ray(ray_eye_to_pixel)
            if rt_colour is not None:
                pt_colour += rt_colour

            # 6. Display results on a grid of pixels
            screen.draw_pixel_col(i, j, np.clip(pt_colour, 0., 1.))

    # print screen.frame_buffer
    screen.write('SV3-raytracer/scene.png')


if __name__ == '__main__':
    main()
