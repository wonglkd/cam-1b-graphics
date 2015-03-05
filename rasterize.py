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
import math
from pprint import pprint


def rasterize_triangle(face, m_matrix=None):
    vertices = [v for v, _ in face]
    # perspective
    if m_matrix is not None:
        vertices = map(lambda v: m_matrix.dot(np.append(v, [0])), vertices)

    # projection onto 2D - strip z value
    vertices = [v[:2] for v in vertices]
    vertices = map(screen.rescale_point, vertices)
    triangle.draw(vertices, wireframe=True)


def gen_m_matrix(camera_pos, look_point, up_vector, d):
    camera_look_dist = np.linalg.norm(camera_pos - look_point)
    d_over_el = d / camera_look_dist
    translation_matrix = np.array([(1, 0, 0, -camera_pos[0, 0]),
                                   (0, 1, 0, -camera_pos[0, 1]),
                                   (0, 0, 1, -camera_pos[0, 2]),
                                   (0, 0, 0, 1)])
    scale_matrix = np.array([(d_over_el, 0, 0, 0),
                             (0, d_over_el, 0, 0),
                             (0, 0, d_over_el, 0),
                             (0, 0, 0,         1)])
    look_point_transformed = scale_matrix.dot(translation_matrix).dot(look_point.T)
    theta = math.acos(look_point_transformed[2, 0] / np.sqrt(look_point_transformed[0, 0] ** 2 + look_point_transformed[2, 0] ** 2))
    theta_cos = math.cos(theta)
    theta_sin = math.sin(theta)
    R_1 = np.array([(theta_cos, 0, -theta_sin, 0),
                    (0, 1, 0, 0),
                    (theta_sin, 0, theta_cos, 0),
                    (0, 0, 0, 1)])
    l_prime_3 = R_1.dot(look_point_transformed)
    phi = math.acos(l_prime_3[2, 0] / np.sqrt(l_prime_3[1, 0] ** 2 + l_prime_3[2, 0] ** 2))
    phi_sin = math.sin(phi)
    phi_cos = math.cos(phi)
    R_2 = np.array([(1, 0, 0, 0),
                    (0, phi_cos, -phi_sin, 0),
                    (0, phi_sin, phi_cos, 0),
                    (0, 0, 0, 1)])
    u_prime_3 = R_2.dot(R_1).dot(up_vector.T)
    psi = math.acos(u_prime_3[1, 0] / np.sqrt(u_prime_3[0, 0] ** 2 + u_prime_3[1, 0] ** 2))
    psi_cos = math.cos(phi)
    phi_sin = math.sin(phi)
    R_3 = np.array([(phi_cos, -phi_sin, 0, 0),
                    (phi_sin, phi_cos, 0, 0),
                    (0, 0, 1, 0),
                    (0, 0, 0, 1)])
    m_matrix = R_3.dot(R_2).dot(R_1).dot(scale_matrix).dot(translation_matrix)
    return m_matrix


def main():
    # d = distance from origin to screen centre
    d = 1.
    # camera_pos = np.array([[0, 0, 0, 0]])
    # look_point = np.array([[0, 0, 1., 0]])
    # up_vector = np.array([[0, 1, 0, 0]])

    # test values
    camera_pos = np.array([[5, 10, 0, 0]])
    look_point = np.array([[5, 10, 1, 0]])
    up_vector = np.array([[5, 15, 1, 0]])
    m_matrix = gen_m_matrix(camera_pos, look_point, up_vector, d)
    print m_matrix

    screen.draw_bounding_box()

    obj = obj_file.load('SV1-utah/wt_teapot.obj')['teapot.005']
    for face in obj.faces:
        try:
            n_face = [(obj.vertices[v], obj.normals[vn]) for v, vn in face]
            rasterize_triangle(n_face, m_matrix=m_matrix)
        except IndexError:
            print "cannot find vertex ",
            pprint(face)
        # draw_triangle([a for a, _ in face])
        # draw_triangle([(1,1),(300,400),(500,400)])
        # draw_triangle([(10+5, 10+10),(10+5,50+10),(10+50,10+10)])
        # draw_triangle([(50, 50),(50+50,50),(50,50+50)])
        # break

    screen.write('SV1-utah/teapot.png')


if __name__ == '__main__':
    main()
