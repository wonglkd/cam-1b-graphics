import bezier
from bezier import Bezier
import screen
from screen import canvas_height, canvas_width


def main():
    # mid_point_circle((175, 175), 150)
    # draw_line_midpoint((0, 0), (150, 150))
    # draw_line_midpoint((0, 0), (150, 100))
    # draw_line_midpoint((0, 0), (100, 150))
    # draw_line((0, 0), (150, 100))
    # draw_line((0, 0), (100, 150))
    # draw_line_midpoint((150, 150), (10, 0))
    # draw_line_midpoint((0, 150), (150, 0))
    bz = Bezier([(5, 5), (100, 100), (200, 100), (300, 5)])
    # draw_bezier_it(bz)
    # draw_bezier_it(bz2)
    bz2 = Bezier([(1, 1),
                  (2 * canvas_height, 1),
                  (-canvas_height, canvas_width - 1),
                  (canvas_height - 1, canvas_width - 1)])
    for epi in (33., 10., 3.3, 1., .33):
        bezier.draw_adaptive(bz2, tolerance=epi)
    screen.write('SV2-curves/bezier.png')

if __name__ == '__main__':
    main()
