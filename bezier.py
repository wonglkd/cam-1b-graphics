import screen
import line
from operator import itemgetter
import numpy as np


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
        return Bezier(pts_q), Bezier(pts_r)

    def is_flat(self, tolerance=.5):
        return (line.is_flat(*itemgetter(0, 3, 1)(self.pts), tolerance=tolerance) and
                line.is_flat(*itemgetter(0, 3, 2)(self.pts), tolerance=tolerance))


def draw_it(bz):
    u = bz.get(.0)
    for t in xrange(5, 100, 5):
        t /= 100.
        v = bz.get(t)
        print v
        line.draw(u, v)
        u = v


def draw_adaptive(bz, tolerance):
    if bz.is_flat(tolerance=tolerance):
        line.draw(bz.pts[0], bz.pts[3])
    else:
        bzs = bz.split()
        for bn in bzs:
            draw_adaptive(bn, tolerance)
