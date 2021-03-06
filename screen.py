import png
import numpy as np
import polygon

dimensions = (350, 350)
canvas_size = (300, 300)
canvas_height, canvas_width = canvas_size

frame_buffer = np.zeros(dimensions, dtype=np.uint8)
z_buffer = np.ones(dimensions, dtype=np.uint8) * np.inf


def draw_pixel(x, y, intensity=1.):
    try:
        frame_buffer[y, x] = intensity * 255
    except IndexError:
        print "Point out of canvas", (x, y)
        raise IndexError


def draw_z_buffer(pt, *args, **kwargs):
    if z_buffer[pt[1], pt[0]] < pt[2]:
        z_buffer[pt[1], pt[0]] = pt[2]
        draw_pixel(pt[0], pt[1], *args, **kwargs)


def draw_bounding_box():
    left_x = 0
    right_x = left_x + canvas_size[0]
    top_y = 0
    bottom_y = top_y + canvas_size[1]
    polygon.draw([(left_x, top_y),
                  (right_x, top_y),
                  (right_x, bottom_y),
                  (left_x, bottom_y)])


def rescale_point(pt):
    """ Rescale points from float to pixel """
    pt[1] *= canvas_size[1]/2.5
    pt[1] += canvas_size[1]/2.
    # pt[1] += (dimensions[1]-canvas_size[1])/2
    pt[0] *= canvas_size[0]/2.5
    pt[0] += canvas_size[0]/2.
    # pt[0] += (dimensions[0]-canvas_size[0])/2
    return pt


def write(filename):
    w = png.Writer(dimensions[0], dimensions[1], greyscale=True)
    with open(filename, 'wb') as f:
        w.write(f, np.flipud(frame_buffer))
