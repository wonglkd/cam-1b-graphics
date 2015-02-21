import png
import numpy as np

dimensions = (350, 350)
canvas_size = (300, 300)

frame_buffer = np.ones(screen_dims, dtype=np.uint8) * 255


def draw_pixel(x, y):
    try:
        frame_buffer[y, x] = 0
    except IndexError:
        print "Point out of canvas", (x, y)


def write(filename):
    w = png.Writer(dimensions[0], dimensions[1], greyscale=True)
    with open('teapot.png', 'wb') as f:
        w.write(f, np.flipud(frame_buffer))
