"""
Polygon rasterizer and shader.

- load object from .obj file.
- polygon rasterization
- implement basic shader

"""
import obj_loader
# from tkinter import Tk, Canvas, Frame, BOTH
import numpy as np
from pprint import pprint


def rescale_point((x, y)):
    y *= canvas_size[1]/2.
    y += canvas_size[1]/2.
    x *= canvas_size[0]/2.
    x += canvas_size[0]/2.
    return x, y


def rasterize_triangle(face):
    vertices = [v for v, _ in face]
    # perspective
    # strip z value
    vertices = [v[:2] for v in vertices]
    vertices = map(rescale_point, vertices)
    draw_triangle(vertices)


def main():
    obj = obj_loader.load('SV1/wt_teapot.obj')['teapot.005']
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
    screen.write('SV1/teapot.png')


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
