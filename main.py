import pygame
from polygon import Polygon
import numpy as np
import globals
from inputs import Inputs
from space import Space
from gui import Window
from PyQt4.QtGui import QApplication
import sys


def main():
    # Initializes pygame, window
    pygame.init()
    window = pygame.display.set_mode((globals.SCREEN_WIDTH, globals.SCREEN_HEIGHT))
    input_params = Inputs()
    clock = pygame.time.Clock()
    app = QApplication(sys.argv)
    param_win = Window()
    param_win.show()

    # Polygon to be controlled by arrows
    polygon = Polygon(np.array([800, 500]), 30, 3, 10, (255, 255, 255))
    space = Space(polygon)
    while globals.RUN:
        # Drawing shapes
        space.draw(window)
        # Adding force to main polygon
        if input_params.is_left():
            polygon.add_force(np.array([-globals.KEY_FORCE, 0.]))
        elif input_params.is_right():
            polygon.add_force(np.array([globals.KEY_FORCE, 0.]))
        if input_params.is_up():
            polygon.add_force(np.array([0., -globals.KEY_FORCE]))
        elif input_params.is_down():
            polygon.add_force(np.array([0., globals.KEY_FORCE]))

        # Add shape on left click
        if input_params.mouse_left_click():
            space.add_shape(globals.NEW_SHAPE_TYPE, input_params.mouse_pos, globals.NEW_SHAPE_RADIUS,
                            globals.NEW_SHAPE_MASS,
                            globals.NEW_SHAPE_DEGREE)
        # Remove shape on right click
        if input_params.mouse_right_click():
            space.remove_shape(input_params.mouse_pos)

        if input_params.is_clear():
            space.shapes = []

        clock.tick(globals.FPS)
        elapsed_time = clock.get_time()
        # Update shapes in space class for movement, rotarion...
        space.update(window, elapsed_time)
        # Check for mouse of keyboard click
        input_params.update()
        pygame.display.update()
        pygame.display.set_caption(str(clock.get_fps()))

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
