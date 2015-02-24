import png
import numpy as np

dimensions = (350, 350)
canvas_size = (300, 300)
canvas_height, canvas_width = canvas_size

frame_buffer = np.zeros((dimensions[0], dimensions[1] * 3), dtype=np.uint8)


def draw_pixel_col(x, y, colour):
    try:
        # print x, y, colour
        frame_buffer[y, (x*3): ((x+1)*3)] = colour * 255
    except IndexError:
        print "Point out of canvas", (x, y)


def rescale_point((x, y)):
    """ Rescale points from float to pixel """
    y *= canvas_size[1]/2.
    y += canvas_size[1]/2.
    x *= canvas_size[0]/2.
    x += canvas_size[0]/2.
    return x, y


def write(filename):
    w = png.Writer(dimensions[0], dimensions[1])
    with open(filename, 'wb') as f:
        w.write(f, frame_buffer)
