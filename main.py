import pygame
from polygon import Polygon
import numpy as np
from runge_kutta import runge_kutta_4
from math import sin
from separating_axis_theorem import check_shapes_collision
import globals
from inputs import Inputs
from circle import Circle
from space import Space
from gui import Window
from PyQt4.QtGui import QApplication
import sys


def main():
    pygame.init()
    window = pygame.display.set_mode((globals.SCREEN_WIDTH, globals.SCREEN_HEIGHT))
    input = Inputs()
    clock = pygame.time.Clock()
    app = QApplication(sys.argv)
    param_win = Window()
    param_win.show()

    polygon = Polygon(np.array([800, 500]), 100, 3, 10., (255, 255, 255))

    space = Space(polygon)
    while globals.RUN:

        space.draw(window)

        # if result is not None:
        #     e = 1.5
        #     vab = polygon.translational_speed - second.translational_speed
        #     rap = result - polygon.centroid
        #     rap = np.array([-rap[1], rap[0]])
        #     rbp = result - second.centroid
        #     rbp = np.array([-rbp[1], rbp[0]])
        #     ia = polygon.moment_area
        #     ib = second.moment_area
        #     a = np.dot(rap, mtv)
        #     b = np.dot(rbp, mtv)
        #
        #     j = (-(1. + e) * vab * mtv) / (
        #                 np.dot(mtv, mtv) * (1 / polygon.mass + 1 / second.mass))  # + pow(a,2) / ia + pow(b,2) / ib)
        #     polygon.translational_speed = polygon.translational_speed + (j / polygon.mass) * mtv
        #     second.translational_speed = second.translational_speed - (j / second.mass) * mtv
        #     # polygon.rotational_speed = polygon.rotational_speed + (np.dot(rap, j*mtv)) / ia
        #     # second.rotational_speed = second.rotational_speed - (np.dot(rbp, j*mtv)) / ib

        #polygon.rotate_reference_vector(0)
        #
        #if input.get_cw():
        #    polygon.add_force(np.array([-100., 1.]), polygon.reference_vector + polygon.centroid)

        if input.is_left():
            polygon.add_force(np.array([-globals.KEY_FORCE, 0.]), polygon.centroid)
        elif input.is_right():
            polygon.add_force(np.array([globals.KEY_FORCE, 0.]), polygon.centroid)
        if input.is_up():
            polygon.add_force(np.array([0., -globals.KEY_FORCE]), polygon.centroid)
        elif input.is_down():
            polygon.add_force(np.array([0., globals.KEY_FORCE]), polygon.centroid)

        if input.mouse_left_click():
            space.add_shape(globals.NEW_SHAPE_TYPE, input.mouse_pos, globals.NEW_SHAPE_RADIUS, globals.NEW_SHAPE_MASS,
                            globals.NEW_SHAPE_DEGREE)
        if input.mouse_right_click():
            space.remove_shape(input.mouse_pos)

        clock.tick(globals.FPS)
        elapsed_time = clock.get_time()
        space.update(window, elapsed_time)
        input.update()
        pygame.display.update()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
