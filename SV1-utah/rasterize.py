"""
Polygon rasterizer and shader.

- load object from .obj file.

"""
from operator import methodcaller


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


def main():
    obj = load_obj_file('wt_teapot.obj')['teapot.005']

if __name__ == '__main__':
    main()
