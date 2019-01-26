import pygame
from polygon import Polygon
import numpy as np
from runge_kutta import runge_kutta_4
from math import sin
from separating_axis_theorem import check_shapes_collision
from circle import Circle

import matplotlib.pyplot


SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 200
MAX_FRAME_TIME = 6 * 1000 / FPS

def update(time, poly):
    poly.update(time)
    pygame.display.update()


def draw(window, polygon, second):

    window.fill((0, 0, 0))
    polygon.draw(window)
    second.draw(window)


# def fun(y, t):
#     return [y[1], (sin(t) + 10 * 9.81 - 100 * y[0] - 30 * y[1]) / 10]


def main():
    pygame.init()
    pygame.display.set_caption('Simulation')
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    run = True

    polygon = Polygon(np.array([800, 500]), 100, 6, 10)
    second = Polygon(np.array([1000, 500]), 100, 7, 10)
    polygon.rotate(np.pi / 4)
    second.rotate(np.pi / 4)
    while run:

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            polygon.forces[0] = np.array([-1000., 0])
        elif keys[pygame.K_RIGHT]:
            polygon.forces[0] = np.array([1000., 0.])
        else:
            polygon.forces[0] = np.array([0., 0.])

        if keys[pygame.K_UP]:
            polygon.forces[1] = np.array([0., -1000.])
        elif keys[pygame.K_DOWN]:
            polygon.forces[1] = np.array([0, 1000.])
        else:
            polygon.forces[1] = np.array([0., 0.])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        clock.tick(FPS)
        elapsed_time = clock.get_time()
        draw(window, polygon, second)

        result = check_shapes_collision(polygon, second)
        if result is not None:
            circle = Polygon(result, 3, 20, 3, color=(0, 255, 0))
            circle.draw(window)

        update(elapsed_time, polygon)




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

