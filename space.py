import pygame
import globals
from circle import Circle
from polygon import Polygon
import numpy as np
from random import randrange
from separating_axis_theorem import check_shapes_collision


class Space:

    def __init__(self, polygon):
        self.polygon = polygon
        self.shapes = []

    def add_shape(self, shape_type, position, radius, mass, degree=3):
        distance = np.sqrt(np.power(abs(self.polygon.centroid[0] - position[0]), 2) + np.power(
            abs(self.polygon.centroid[1] - position[1]), 2))
        if distance <= radius + self.polygon.radius:
            return

        for shape in self.shapes:
            distance = np.sqrt(
                np.power(abs(shape.centroid[0] - position[0]), 2) + np.power(abs(shape.centroid[1] - position[1]), 2))
            if distance <= radius + shape.radius:
                return

        if shape_type == globals.ShapeType.CIRCLE:
            shape = Circle(np.array(position), radius, mass, (randrange(0, 255), randrange(0, 255), randrange(0, 255)))
        elif shape_type == globals.ShapeType.POLYGON:
            shape = Polygon(np.array(position), radius, degree, mass,
                            (randrange(0, 255), randrange(0, 255), randrange(0, 255)))
        else:
            raise Exception('Wrong shape')
        self.shapes.append(shape)

    def remove_shape(self, position):
        for shape in self.shapes:
            distance = np.sqrt(
                np.power(abs(shape.centroid[0] - position[0]), 2) + np.power(abs(shape.centroid[1] - position[1]), 2))
            if distance < shape.radius:
                self.shapes.remove(shape)
                break

    def draw(self, window):
        window.fill((0, 0, 0))
        self.polygon.draw(window)
        for shape in self.shapes:
            shape.draw(window)

    def update(self, window, time):
        self.polygon.update(time)
        for shape in self.shapes:
            result = check_shapes_collision(self.polygon, shape)
            if result is not None:
                pygame.draw.circle(window, (0, 255, 0), result[0].astype(int), 3)

    # Ovde cemo za svaki shape uraditi odbijanje od ivice
    def check_borders(self):
        # for shape in self.shapes:
        #     pass
        pass