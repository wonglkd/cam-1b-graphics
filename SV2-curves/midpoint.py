from operator import methodcaller
from operator import itemgetter
# from tkinter import Tk, Canvas, Frame, BOTH
import numpy as np
# import matplotlib
# import matplotlib.pyplot as plt
import png
from pprint import pprint

canvas_size = (300, 300)
canvas_height, canvas_width = canvas_size
screen_dims = (canvas_size[0] + 50, canvas_size[1] + 50)
frame_buffer = np.ones(screen_dims, dtype=np.uint8) * 255


def draw_pixel(x, y):
    try:
        frame_buffer[y, x] = 0
    except IndexError:
        print "Point out of canvas", (x, y)


def mid_point_circle(centre, radius):
    x_0, y_0 = centre
    x, y = radius, 0
    radius_error = 1 - x
    while x >= y:
        types = [(x, y), (-x, y), (-y, x), (-x, -y)]
        for a, b in types:
            draw_pixel(a + x_0, b + y_0)
            draw_pixel(b + x_0, a + y_0)

        y += 1
        if radius_error < 0:
            radius_error += 2 * y + 1
        else:
            x -= 1
            radius_error += 2 * (y - x) + 1


def draw_line(u, v):
    x_0, y_0 = map(int, u)
    x_1, y_1 = map(int, v)
    d_x = abs(x_1 - x_0)
    d_y = abs(y_1 - y_0)
    s_x = 1 if x_0 < x_1 else -1
    s_y = 1 if y_0 < y_1 else -1
    err = d_x - d_y
    while True:
        draw_pixel(x_0, y_0)
        if x_0 == x_1 and y_0 == y_1:
            break
        e2 = 2 * err
        if e2 > -d_y:
            err -= d_y
            x_0 += s_x
        if e2 < d_x:
            err += d_x
            y_0 += s_y


def is_flat_line(pt_a, pt_b, pt_c, tolerance=.5):
    v_ab = pt_b - pt_a
    v_ac = pt_c - pt_a
    s = np.dot(v_ab, v_ac) / float(np.sum(v_ab ** 2))
    if s < 0 or s > 1:
        return False
    pt_p = (1. - s) * pt_a + s * pt_b
    v_cp = pt_p - pt_c
    return np.linalg.norm(v_cp) < tolerance


class Bezier(object):
    """Bezier Curve - defined by two end points and two control points."""
    def __init__(self, pts):
        if len(pts) != 4:
            raise ValueError(len(pts))
        self.pts = [np.array(pt) for pt in pts]

    def get(self, t):
        if not (.0 <= t and t <= 1.):
            raise ValueError
        return tuple(
            pow(1 - t, 3) * self.pts[0]
            + 3 * t * pow(1 - t, 2) * self.pts[1]
            + 3 * pow(t, 2) * (1 - t) * self.pts[2]
            + pow(t, 3) * self.pts[3]
        )

    def split(self):
        pts_q = [self.pts[0],
                 self.pts[0] / 2. + self.pts[1] / 2.,
                 self.pts[0] / 4. + self.pts[1] / 2. + self.pts[2] / 4.,
                 self.pts[0] / 8. + self.pts[1] * 3. / 8. + self.pts[2] * 3. / 8. + self.pts[3] / 8.]
        pts_r = [self.pts[0] / 8. + self.pts[1] * 3. / 8. + self.pts[2] * 3. / 8. + self.pts[3] / 8.,
                 self.pts[1] / 4. + self.pts[2] / 2. + self.pts[3] / 4.,
                 self.pts[2] / 2. + self.pts[3] / 2.,
                 self.pts[3]]
        print pts_q
        print pts_r
        return Bezier(pts_q), Bezier(pts_r)

    def is_flat(self, tolerance=.5):
        return (is_flat_line(*itemgetter(0, 3, 1)(self.pts), tolerance=tolerance) and
                is_flat_line(*itemgetter(0, 3, 2)(self.pts), tolerance=tolerance))


def draw_bezier_it(bz):
    u = bz.get(.0)
    for t in xrange(5, 100, 5):
        t /= 100.
        v = bz.get(t)
        print v
        draw_line(u, v)
        u = v


def draw_bezier_adaptive(bz, tolerance):
    if bz.is_flat(tolerance=tolerance):
        draw_line(bz.pts[0], bz.pts[3])
    else:
        bzs = bz.split()
        for bn in bzs:
            draw_bezier_adaptive(bn, tolerance)


def rescale_point((x, y)):
    y *= canvas_size[1]/2.
    y += canvas_size[1]/2.
    x *= canvas_size[0]/2.
    x += canvas_size[0]/2.
    return x, y


def main():
    mid_point_circle((175, 175), 150)
    print is_flat_line(np.array([0, 1]), np.array([5, 1]), np.array([4, 1]))
    w = png.Writer(screen_dims[0], screen_dims[1], greyscale=True)
    with open('sv2.png', 'wb') as f:
        w.write(f, np.flipud(frame_buffer))

if __name__ == '__main__':
    main()
