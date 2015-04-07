import numpy as np
from primitives import Vector
from common import normalize


def specular(v, v_n, view_pt, light_pt, coef=10):
    v_n /= normalize(v_n)
    view_pt = view_pt[0][:3]
    v_i = v - light_pt
    v_i /= normalize(v_i)

    v_reflected = -v_i - 2 * -v_i.dot(v_n) * v_n
    v_viewer = Vector(view_pt - v).normalized().dir
    intensity_specular = max(v_reflected.dot(v_viewer), 0.)
    intensity_specular = pow(intensity_specular, coef)
    return intensity_specular
