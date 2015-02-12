"""
Polygon rasterizer and shader.

- load object from .obj file.
- polygon rasterization
- implement basic shader

"""
from operator import methodcaller
# from tkinter import Tk, Canvas, Frame, BOTH
import numpy as np
# import matplotlib
# import matplotlib.pyplot as plt
import png
from pprint import pprint


class Obj(object):
    vertices = []
    normals = []
    faces = []


def load_obj_file(filename):
    curr_obj = None
    objs = {}
    smoothing_grp = None
    with open(filename, 'r') as f:
        for line in f:
            if line.startswith('#'):
                continue
            line = line.split()

            if line[0] == 'o':
                # introduce new object
                curr_obj_name = line[1]
                objs[curr_obj_name] = Obj()
                curr_obj = objs[curr_obj_name]
            elif not curr_obj:
                raise ValueError("no object introduced using 'o'")

            if line[0] == 'v':
                # vertex (x : float, y : float, z : float)
                v = map(float, line[1:4])
                curr_obj.vertices.append(v)
            elif line[0] == 'vn':
                # normal (x : float, y : float, z : float)
                vn = map(float, line[1:4])
                curr_obj.normals.append(vn)
            elif line[0] == 's':
                s_grp = line[1]
                if s_grp == 'off' or s_grp == '0':
                    smoothing_grp = None
                else:
                    smoothing_grp = int(s_grp)
                # TODO: full implementation of shading group
            elif line[0] == 'f':
                # faces - using vertex indices (e.g. 34//1 1243//2 593//3)
                if '//' in line[1]:
                    face = map(methodcaller('split', '//'), line[1:4])
                    face = map(lambda x: map(int, x), face)
                else:
                    raise NotImplementedError
                curr_obj.faces.append(face)
    return objs


screen_dims = (350, 350)
canvas_size = (300, 300)
# frame_buffer = np.zeros((screen_dims[0], screen_dims[1], 3), dtype=np.uint8)
frame_buffer = np.ones(screen_dims, dtype=np.uint8) * 255


def draw_pixel(x, y):
    y *= canvas_size[1]/2.
    y += canvas_size[1]/2.
    x *= canvas_size[0]/2.
    x += canvas_size[0]/2.

    try:
        frame_buffer[y, x] = 0
    except IndexError:
        print "Point out of canvas", (x, y)


def draw_triangle(vertices):
    v1, v2, v3 = vertices
    vs1 = v2[0]-v1[0], v2[1]-v1[1]
    vs2 = v3[0]-v1[0], v3[1]-v1[1]

    for v in vertices:
        v[1] -= .1
        draw_pixel(*v)
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
                draw_pixel(i, j)


def rasterize_triangle(face):
    vertices = [v for v, _ in face]
    # perspective
    # strip z value
    vertices = [v[:2] for v in vertices]
    draw_triangle(vertices)


def main():
    obj = load_obj_file('wt_teapot.obj')['teapot.005']
    for face in obj.faces:
        try:
            n_face = [(obj.vertices[v], obj.normals[vn]) for v, vn in face]
            rasterize_triangle(n_face)
        except IndexError:
            print "cannot find vertex ",
            pprint(face)
        # draw_triangle([a for a, _ in face])
        # draw_triangle([(1,1),(300,400),(500,400)])
        # draw_triangle([(10+5, 10+10),(10+5,50+10),(10+50,10+10)])
        # draw_triangle([(50, 50),(50+50,50),(50,50+50)])
        # break

    # T = np.array((1, 0, 0, -e[0]),
    #              (0, 1, 0, -e[1]),
    #              (0, 0, 0, 1))

    w = png.Writer(screen_dims[0], screen_dims[1], greyscale=True)
    with open('teapot.png', 'wb') as f:
        w.write(f, np.flipud(frame_buffer))

    # plt.imshow(matrix) #Needs to be in row,col order
    # plt.show()
    # plt.savefig(filename)


# def main():

# class Example(Frame):
#     def __init__(self, parent):
#         Frame.__init__(self, parent)

#         self.parent = parent
#         self.initUI()

#     def initUI(self):
#         self.parent.title("Colors")
#         self.pack(fill=BOTH, expand=1)

#         canvas = Canvas(self)
#         canvas.create_rectangle(30, 10, 120, 80,
#                                 outline="#fb0", fill="#fb0")
#         canvas.create_rectangle(150, 10, 240, 80,
#                                 outline="#f50", fill="#f50")
#         canvas.create_rectangle(270, 10, 370, 80,
#                                 outline="#05f", fill="#05f")
#         canvas.pack(fill=BOTH, expand=1)


# def main():
#     root = Tk()
#     ex = Example(root)
#     root.geometry("400x100+300+300")
#     root.mainloop()



if __name__ == '__main__':
    main()
