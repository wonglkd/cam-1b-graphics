from operator import methodcaller
# from tkinter import Tk, Canvas, Frame, BOTH
import numpy as np
# import matplotlib
# import matplotlib.pyplot as plt
import png
from pprint import pprint

screen_dims = (350, 350)
canvas_size = (300, 300)
# frame_buffer = np.zeros((screen_dims[0], screen_dims[1], 3), dtype=np.uint8)
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


def rescale_point((x, y)):
    y *= canvas_size[1]/2.
    y += canvas_size[1]/2.
    x *= canvas_size[0]/2.
    x += canvas_size[0]/2.
    return x, y


def main():
    mid_point_circle((175, 175), 150)
    w = png.Writer(screen_dims[0], screen_dims[1], greyscale=True)
    with open('sv2.png', 'wb') as f:
        w.write(f, np.flipud(frame_buffer))

if __name__ == '__main__':
    main()
