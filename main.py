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

    polygon = Polygon(np.array([800, 500]), 100, 6, 1.)
    second = Polygon(np.array([1000, 500]), 100, 7, 100.)
    polygon.rotate(np.pi / 4)
    second.rotate(np.pi / 4)
    while globals.RUN:

        polygons = [polygon, second]
        collision = check_shapes_collision(polygon, second)
        result = collision[0] if collision is not None else None
        mtv = collision[1] if collision is not None else None
        draw(window, polygons)

        if result is not None:
            e = 1.5
            vab = polygon.translational_speed - second.translational_speed
            rap = result - polygon.centroid
            rap = np.array([-rap[1], rap[0]])
            rbp = result - second.centroid
            rbp = np.array([-rbp[1], rbp[0]])
            ia = polygon.moment_area
            ib = second.moment_area
            a = np.dot(rap, mtv)
            b = np.dot(rbp, mtv)

            j = (-(1. + e) * vab * mtv) / (
                        np.dot(mtv, mtv) * (1 / polygon.mass + 1 / second.mass))  # + pow(a,2) / ia + pow(b,2) / ib)
            polygon.translational_speed = polygon.translational_speed + (j / polygon.mass) * mtv
            second.translational_speed = second.translational_speed - (j / second.mass) * mtv
            # polygon.rotational_speed = polygon.rotational_speed + (np.dot(rap, j*mtv)) / ia
            # second.rotational_speed = second.rotational_speed - (np.dot(rbp, j*mtv)) / ib

        polygon.rotate_reference_vector(0)
        #
        if input.get_cw():
            polygon.add_force(np.array([-100., 1.]), polygon.reference_vector + polygon.centroid)

        if input.get_left():
            polygon.add_force(np.array([-1000., 0.]), polygon.centroid)
        elif input.get_right():
            polygon.add_force(np.array([1000., 0.]), polygon.centroid)

        if input.get_up():
            polygon.add_force(np.array([0., -1000.]), polygon.centroid)
        elif input.get_down():
            polygon.add_force(np.array([0., 1000.]), polygon.centroid)


        clock.tick(globals.FPS)
        elapsed_time = clock.get_time()
        draw(window, polygons)
        if result is not None:
            circle = Polygon(result, 3, 20, 3, color=(0, 255, 0))
            circle.draw(window)

        circle = Polygon(polygon.reference_vector + polygon.centroid, 3, 20, 3, color = (0, 255, 0))
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

