import screen


def draw_midpoint(centre, radius):
    x_0, y_0 = centre
    x, y = radius, 0
    radius_error = 1 - x
    while x >= y:
        types = [(x, y), (-x, y), (-y, x), (-x, -y)]
        for a, b in types:
            screen.draw_pixel(a + x_0, b + y_0)
            screen.draw_pixel(b + x_0, a + y_0)

        y += 1
        if radius_error < 0:
            radius_error += 2 * y + 1
        else:
            x -= 1
            radius_error += 2 * (y - x) + 1
