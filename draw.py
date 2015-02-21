import screen
import numpy as np


def line(v, u):
    x_0, y_0 = v
    x_1, y_1 = u
    if x_1 - x_0 == 0:
        return
        # v, u = u, v
        # x_0, y_0 = v
        # x_1, y_1 = u
        # if x_1 - x_0 == 0:
        #     return

    m = (y_1 - y_0) / (x_1 - x_0)

    x = round(x_0)
    y_i = y_0 + m * (x - x_0)

    y = round(y_i)
    y_f = y_i - y

    while x <= round(x_1):
        screen.draw_pixel(x, y)
        x += 1
        y_f += m
        if y_f > .5:
            y += 1
            y_f -= 1


def triangle(vertices):
    v1, v2, v3 = vertices
    vs1 = v2[0]-v1[0], v2[1]-v1[1]
    vs2 = v3[0]-v1[0], v3[1]-v1[1]

    for v in vertices:
        screen.draw_pixel(*v)
    for v, u in zip(vertices, vertices[1:] + [vertices[0]]):
        line(v, u)
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
                screen.draw_pixel(i, j)
