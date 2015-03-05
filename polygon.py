import line


def draw(vertices):
    vertices_a = vertices + [vertices[0]]
    for v, v_n in zip(vertices_a, vertices_a[1:]):
        line.draw(v, v_n)
