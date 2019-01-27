import pygame
from polygon import Polygon
import numpy as np
from runge_kutta import runge_kutta_4
from math import sin
from separating_axis_theorem import check_shapes_collision
import globals
from inputs import Inputs
from circle import Circle

import matplotlib.pyplot


SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 200
MAX_FRAME_TIME = 6 * 1000 / FPS

def update(time, poly, input):
    input.update()
    #poly.update(time)
    for p in poly:
        p.update(time)
    pygame.display.update()


def draw(window, polygon):

    window.fill((0, 0, 0))
    for p in polygon:
        p.draw(window)
    #polygon.draw(window)


# def fun(y, t):
#     return [y[1], (sin(t) + 10 * 9.81 - 100 * y[0] - 30 * y[1]) / 10]


def main():
    pygame.init()
    window = pygame.display.set_mode((globals.SCREEN_WIDTH, globals.SCREEN_HEIGHT))
    input = Inputs()
    globals.RUN = True
    clock = pygame.time.Clock()
    globals.RUN = True

    polygon = Polygon(np.array([800, 500]), 100, 6, 100.)
    second = Polygon(np.array([1000, 500]), 100, 7, 100.)
    polygon.rotate(np.pi / 4)
    second.rotate(np.pi / 4)
    while globals.RUN:

        polygons = [polygon, second]
        result = check_shapes_collision(polygon, second)

        second.add_force(np.array([np.array([-100., 0.]), second.centroid]))

        if input.get_cw() == True:
            polygon.add_force(np.array([second.forces[1][0], result]))
            second.add_force(np.array([polygon.forces[1][0], result]))

        if input.get_left():
            #polygon.translational_forces[0] = polygon.translational_forces[0] + np.array([-1000., 0.])
            polygon.add_force(np.array([np.array([-1000., 0.]), polygon.centroid]))
        elif input.get_right():
            #polygon.translational_forces[0] = polygon.translational_forces[0] + np.array([1000., 0.])
            polygon.add_force(np.array([np.array([1000., 0.]), polygon.centroid]))

        if input.get_up():
            #polygon.translational_forces[1] = np.array([0., -1000.])
            polygon.add_force(np.array([np.array([0., -1000.]), polygon.centroid]))
        elif input.get_down():
            #polygon.translational_forces[1] = np.array([0., 1000.])
            polygon.add_force(np.array([np.array([0., 1000.]), polygon.centroid]))


        clock.tick(globals.FPS)
        elapsed_time = clock.get_time()
        draw(window, polygons)
        if result is not None:
            circle = Polygon(result, 3, 20, 3, color=(0, 255, 0))
            circle.draw(window)
        update(elapsed_time, polygons, input)




def fun(y):
    return [y[1], (0 - 0 * y[1])/20]


if __name__ == '__main__':
    main()
    #axis = np.array([-0.7071067811871176, 0.7071067811859774])
    #print round(5.49, 0)
    # vertex = np.array([50, 50])
    # second = np.array([52, 49])
    # print (vertex <= second).all()
    # print runge_kutta_4_step(fun, 0.01, [10, 50])
    # y = [1, 1]
    # Y =[[], []]
    # time = np.arange(0.0, 40.0, 0.1)
    # for t in time:
    #
    #     #if t == time[0]:
    #
    #
    #     y = [y[i] + runge_kutta_4_step(fun, 0.1, t, y)[i] for i in range(len(y))]
    #
    #     Y[0].append(y[0])
    #     Y[1].append(y[1])
    #
    # matplotlib.pyplot.plot(time, Y[0])
    # matplotlib.pyplot.plot(time, Y[1])
    # matplotlib.pyplot.show()

