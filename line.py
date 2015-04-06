import screen
import numpy as np


def is_flat(pt_a, pt_b, pt_c, tolerance=.5):
    v_ab = pt_b - pt_a
    v_ac = pt_c - pt_a
    s = np.dot(v_ab, v_ac) / float(np.sum(v_ab ** 2))
    if s < 0 or s > 1:
        return False
    pt_p = (1. - s) * pt_a + s * pt_b
    v_cp = pt_p - pt_c
    return np.linalg.norm(v_cp) < tolerance


def draw(u, v):
    """ Placeholder, to replace with draw_midpoint once that is debugged. """
    u = map(int, u[:2])
    v = map(int, v[:2])
    x_0, y_0 = map(int, u)
    x_1, y_1 = map(int, v)
    d_x = abs(x_1 - x_0)
    d_y = abs(y_1 - y_0)
    s_x = 1 if x_0 < x_1 else -1
    s_y = 1 if y_0 < y_1 else -1
    err = d_x - d_y
    try:
        while True:
            screen.draw_pixel(x_0, y_0)
            if x_0 == x_1 and y_0 == y_1:
                break
            e2 = 2 * err
            if e2 > -d_y:
                err -= d_y
                x_0 += s_x
            if e2 < d_x:
                err += d_x
                y_0 += s_y
    except ValueError:
        print "Failed to draw line ", u, v
        raise ValueError


def draw_b(v, u):
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
        screen.screen.draw_pixel(x, y)
        x += 1
        y_f += m
        if y_f > .5:
            y += 1
            y_f -= 1



# def draw_line_midpoint(u, v):
#     x_0, y_0 = u
#     x_1, y_1 = v

#     d_x = abs(x_1 - x_0)
#     d_y = abs(y_1 - y_0)
#     a = y_1 - y_0
#     b = -(x_1 - x_0)
#     c = x_1 * y_0 - x_0 * y_1
#     x = round(x_0)
#     y = round((-a * x - c) / b)
#     dx = 1 if x_0 < x_1 else -1
#     dy = 1 if y_0 < y_1 else -1
#     d = a * (x + dx) + b * (y + .5 * dy) + c

#     while x <= round(x_1):
#         screen.draw_pixel(x, y)
#         if d < 0:
#             d += a
#         else:
#             d += a + b
#             y += dy
#         x += dx


# def draw_line_midpoint_first_oct(u, v):
#     x_0, y_0 = u
#     x_1, y_1 = v

#     a = y_1 - y_0
#     b = -(x_1 - x_0)
#     c = x_1 * y_0 - x_0 * y_1
#     x = round(x_0)
#     y = round((-a * x - c) / b)
#     if abs(b) >= abs(a):
#         dx, dy = 1., .5
#     else:
#         dx, dy = .5, 1.
#     if x_0 > x_1:
#         dx *= -1.
#     if y_0 > y_1:
#         dy *= -1
#     d = a * (x + dx) + b * (y + dy) + c

#     while True:
#         screen.draw_pixel(x, y)
#         if d < 0:
#             d += a
#         else:
#             d += a + b
#             y += dy
#         x += dx