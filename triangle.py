import screen
import line
import numpy as np
from common import normalize


def draw_wireframe(vertices):
    for v in vertices:
        screen.draw_pixel(*v[:2])
    for v, u in zip(vertices, vertices[1:] + [vertices[0]]):
        line.draw(v[:2], u[:2])


def draw_barycentric(vertices, shading_func):
    vertices = [map(int, v) for v in vertices]
    v1, v2, v3 = vertices
    vs1 = v2[0] - v1[0], v2[1] - v1[1]
    vs2 = v3[0] - v1[0], v3[1] - v1[1]
    # calculate bounding box
    max_x = int(max(v[0] for v in vertices))
    min_x = int(min(v[0] for v in vertices))
    max_y = int(max(v[1] for v in vertices))
    min_y = int(min(v[1] for v in vertices))

    # iterate over each point inside bounding box
    for i in range(min_x, max_x + 1):
        for j in range(min_y, max_y + 1):
            v = (i - v1[0], j - v1[1])
            n1 = float(np.cross(v, vs2)) / np.cross(vs1, vs2)
            n2 = float(np.cross(vs1, v)) / np.cross(vs1, vs2)

            if n1 >= 0 and n2 >= 0 and n1 + n2 <= 1:
                screen.draw_pixel(i, j, shading_func((i, j)))


def draw_rec_bottomflat(vertices, shading_func):
    v1, v2, v3 = vertices
    invslope1 = (v2[0] - v1[0]) / float(v2[1] - v1[1])
    invslope2 = (v3[0] - v1[0]) / float(v3[1] - v1[1])

    curr_x1, curr_x2 = float(v1[0]), float(v1[0])
    for scan_y in xrange(int(v1[1]), int(v2[1] + 1)):
        line.draw((curr_x1, scan_y), (curr_x2, scan_y), shading_func)
        curr_x1 += invslope1
        curr_x2 += invslope2


def draw_rec_topflat(vertices, shading_func):
    v1, v2, v3 = vertices
    invslope1 = (v3[0] - v1[0]) / float(v3[1] - v1[1])
    invslope2 = (v3[0] - v2[0]) / float(v3[1] - v2[1])

    curr_x1, curr_x2 = float(v3[0]), float(v3[0])
    for scan_y in xrange(int(v3[1]), int(v1[1]), -1):
        curr_x1 -= invslope1
        curr_x2 -= invslope2
        line.draw((curr_x1, scan_y), (curr_x2, scan_y), shading_func)


def draw_rec(vertices, shading_func, *args, **kwargs):
    vertices = sorted(vertices, key=lambda x: x[1])
    vertices = [map(int, v) for v in vertices]
    v1, v2, v3 = vertices
    if v2[1] == v3[1]:
        if v1[1] == v2[1]:
            # collinear
            line.draw(v1, v2, shading_func)
            line.draw(v2, v3, shading_func)
            line.draw(v1, v3, shading_func)
        else:
            draw_rec_bottomflat(vertices, shading_func)
    elif v1[1] == v2[1]:
        draw_rec_topflat(vertices, shading_func)
    else:
        v4 = (v1[0] + (v2[1] - v1[1]) / float(v3[1] - v1[1]) * (v3[0] - v1[0]),
              v2[1])
        v4 = map(int, v4)
        try:
            draw_rec_bottomflat([v1, v2, v4], shading_func)
            draw_rec_topflat([v2, v4, v3], shading_func)
        except RuntimeError:
            print([v1, v2, v4])
            print v4
            raise RuntimeError


def interpolate(v, vertices):
    v = np.asarray(v)
    v1, v2, v3 = vertices
    T = np.matrix([[v1[0] - v3[0], v2[0] - v3[0]],
                  [v1[1] - v3[1], v2[1] - v3[1]]])
    sol = T.I * np.matrix(v - vertices[2][:2]).T
    sol = np.array(sol).ravel().tolist() + [1. - sol.sum()]
    np.clip(sol, 0., 1.)
    return sol


def draw(vertices, wireframe=False, shading=1., shadings=None, *args, **kwargs):
    if wireframe:
        draw_wireframe(vertices)
    else:
        if shadings:
            def shading_func(u):
                pt = np.array(u)
                dists = [normalize(v[:2] - pt) for v in vertices]
                l_shading = 0.
                weights = interpolate(pt, vertices)
                for weight, shade in zip(weights, shadings):
                    l_shading += weight/sum(weights) * shade
                return l_shading
        else:
            shading_func = lambda _: shading
        try:
            draw_rec(vertices, shading_func)
            # draw_barycentric(vertices, shading_func, *args, **kwargs)
        except RuntimeError:
            print "Failed to draw triangle ", vertices
