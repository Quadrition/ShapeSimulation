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
