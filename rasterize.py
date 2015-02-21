"""
Polygon rasterizer and shader.

- load object from .obj file.
- polygon rasterization
- implement basic shader

"""
import obj_file
import screen
import triangle
import numpy as np
from pprint import pprint


def rasterize_triangle(face):
    vertices = [v for v, _ in face]
    # perspective
    # strip z value
    vertices = [v[:2] for v in vertices]
    vertices = map(screen.rescale_point, vertices)
    triangle.draw(vertices)


def main():
    obj = obj_file.load('SV1-utah/wt_teapot.obj')['teapot.005']
    for face in obj.faces:
        try:
            n_face = [(obj.vertices[v], obj.normals[vn]) for v, vn in face]
            rasterize_triangle(n_face)
        except IndexError:
            print "cannot find vertex ",
            pprint(face)
        # draw_triangle([a for a, _ in face])
        # draw_triangle([(1,1),(300,400),(500,400)])
        # draw_triangle([(10+5, 10+10),(10+5,50+10),(10+50,10+10)])
        # draw_triangle([(50, 50),(50+50,50),(50,50+50)])
        # break

    # T = np.array((1, 0, 0, -e[0]),
    #              (0, 1, 0, -e[1]),
    #              (0, 0, 0, 1))
    screen.write('SV1-utah/teapot.png')


if __name__ == '__main__':
    main()
