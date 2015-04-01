import screen
import line
import numpy as np
from common import normalize


def draw(vertices, wireframe=False, shading=1., shadings=None):
    v1, v2, v3 = vertices
    vs1 = v2[0]-v1[0], v2[1]-v1[1]
    vs2 = v3[0]-v1[0], v3[1]-v1[1]

    if wireframe:
        for v in vertices:
            screen.draw_pixel(v[:2])
        for v, u in zip(vertices, vertices[1:] + [vertices[0]]):
            line.draw(v[:2], u[:2])
        return

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
                if shadings:
                    pt = np.array([i, j])
                    dists = [normalize(v[:2] - pt) for v in vertices]
                    shading = 0.
                    for dist, shade in zip(dists, shadings):
                        shading += dist/sum(dists) * shade
                    # print dists, shadings, shading
                screen.draw_pixel(i, j, shading)
