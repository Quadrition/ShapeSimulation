import pygame
from polygon import Polygon
import math
from vector import Vector
import numpy as np
from runge_kutta import runge_kutta_4
from math import sin

import matplotlib.pyplot


SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
MAX_FRAME_TIME = 6 * 1000 / FPS

def update(time, poly):
    poly.update(time)
    pygame.display.update()


def draw(window, polygon):

    window.fill((0, 0, 0))
    polygon.draw(window)


# def fun(y, t):
#     return [y[1], (sin(t) + 10 * 9.81 - 100 * y[0] - 30 * y[1]) / 10]


def main():
    pygame.init()
    pygame.display.set_caption('Simulation')
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    run = True
    polygon = Polygon(np.array([50, 50]), 10, 4, 1)
    while run:

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            polygon.force[0] = 500
            polygon.angles[0] = math.pi
        elif keys[pygame.K_RIGHT]:
            polygon.force[0] = 500
            polygon.angles[0] = 0
        else:
            polygon.force[0] = 0
            polygon.angles[0] = 0#.5 * math.pi

        if keys[pygame.K_UP]:
            polygon.force[1] = 500
            polygon.angles[1] = -0.5 * math.pi
        elif keys[pygame.K_DOWN]:
            polygon.force[1] = 500
            polygon.angles[1] = 0.5 * math.pi
        else:
            polygon.force[1] = 0
            polygon.angles[1] = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        clock.tick(FPS)
        elapsed_time = clock.get_time()
        draw(window, polygon)
        update(elapsed_time, polygon)

def fun(y):
    return [y[1], (0 - 0 * y[1])/20]


if __name__ == '__main__':
    main()

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

