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
        print self.polygon.translational_speed
        self.polygon.update(time)
        for shape in self.shapes:
            shape.update(time)
            result = check_shapes_collision(self.polygon, shape)
            if result is not None:
                self.resolve_collision(self.polygon, shape, result[0], result[1])
                pygame.draw.circle(window, (0, 255, 0), result[0].astype(int), 3)


    # RESAVA SUDAR PREKO IMPULSA
    def resolve_collision(self, first, second, collision_point, n):
        e = 1.
        r_ap = collision_point - first.centroid
        r_bp = collision_point - second.centroid
        r_ap_perpendicular = np.array([-r_ap[1], r_ap[0]])  # OVE DVE PROMENLJIVE
        r_bp_perpendicular = np.array([-r_bp[1], r_bp[0]])  # NEMOJ JOS BRISATI
        invm_a = 1. / first.mass
        invm_b = 1. / second.mass
        velocity_a = first.translational_speed  # + first.rotational_speed * r_ap_perpendicular # PROBAJ BEZ I SA ISKOMENTARISANIM
        velocity_b = second.translational_speed  # + second.rotational_speed * r_bp_perpendicular # TAKODJE I OVDE
        velocity = velocity_a - velocity_b
        incercy_a = np.power(np.dot(r_ap_perpendicular, n), 2) / first.moment_area
        incercy_b = np.power(np.dot(r_bp_perpendicular, n), 2) / second.moment_area
        impulse_numerator = -(1. + e) * np.dot(velocity, n)
        impulse_denominator = ((invm_a + invm_b) * np.dot(n, n)) #+ incercy_a + incercy_b
        impulse = impulse_numerator / impulse_denominator

        first.translational_speed = first.translational_speed + invm_a * impulse * n
        second.translational_speed = second.translational_speed - invm_b * impulse * n

        impulse_denominator = ((invm_a + invm_b) * np.dot(n, n)) + incercy_a + incercy_b
        impulse = impulse_numerator / impulse_denominator

        first.rotational_speed = first.rotational_speed - np.dot(r_ap_perpendicular, (impulse * n)) / first.moment_area
        second.rotational_speed = second.rotational_speed + np.dot(r_bp_perpendicular, (impulse * n)) / second.moment_area
        #first.

    # Ovde cemo za svaki shape uraditi odbijanje od ivice
    def check_borders(self):
        # for shape in self.shapes:
        #     pass
        pass
