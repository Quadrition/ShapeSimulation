import pygame
import globals
from circle import Circle
from polygon import Polygon
import numpy as np
from random import randrange
from separating_axis_theorem import check_shapes_collision, check_border
from spatial_indexing import QuadTree


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
        tree = QuadTree()
        self.resolve_border_collision(self.polygon)
        self.polygon.update(time)
        tree.add_shape(self.polygon)
        for i in range(len(self.shapes)):
            # text_to_screen(window, i, self.shapes[i].centroid[0], self.shapes[i].centroid[1])
            self.resolve_border_collision(self.shapes[i])
            self.shapes[i].update(time)
            tree.add_shape(self.shapes[i])

        # count = 0
        collision = tree.find_collision_points()
        for col in collision:
            for i in range(len(col[0])):
                for j in range(i + 1, len(col[0])):
                    # count += 1
                    result = check_shapes_collision(col[0][i], col[0][j])
                    if result is not None:
                        self.resolve_collision(col[0][i], col[0][j], result[0], result[1])
                for j in range(len(col[1])):
                    # count += 1
                    result = check_shapes_collision(col[0][i], col[1][j])
                    if result is not None:
                        self.resolve_collision(col[0][i], col[1][j], result[0], result[1])

        # print count
        # tree.draw_bars(window, tree.root)

    # RESAVA SUDAR PREKO IMPULSA
    @staticmethod
    def resolve_collision(first, second, collision_point, n):
        e = 0.5
        r_ap = collision_point - first.centroid
        r_bp = collision_point - second.centroid
        r_ap_perpendicular = np.array([-r_ap[1], r_ap[0]])
        r_bp_perpendicular = np.array([-r_bp[1], r_bp[0]])
        invm_a = 1. / first.mass
        invm_b = 1. / second.mass
        velocity_a = first.translational_speed  # + first.rotational_speed * r_ap_perpendicular
        velocity_b = second.translational_speed  # + second.rotational_speed * r_bp_perpendicular
        velocity = velocity_a - velocity_b

        # if np.dot(velocity, n) < 0:
        #     return

        moment_area_a = np.power(np.dot(r_ap_perpendicular, n), 2) / first.moment_area
        moment_area_b = np.power(np.dot(r_bp_perpendicular, n), 2) / second.moment_area
        impulse_numerator = -(1. + e) * np.dot(velocity, n)
        impulse_denominator = ((invm_a + invm_b) * np.dot(n, n)) + moment_area_a + moment_area_b
        impulse = impulse_numerator / impulse_denominator

        first.translational_speed = first.translational_speed + invm_a * impulse * n
        second.translational_speed = second.translational_speed - invm_b * impulse * n

        # impulse_denominator = ((invm_a + invm_b) * np.dot(n, n)) + moment_area_a + moment_area_b
        # impulse = impulse_numerator / impulse_denominator

        first.rotational_speed += -np.dot(r_ap_perpendicular, (impulse * n)) / first.moment_area
        second.rotational_speed += np.dot(r_bp_perpendicular, (impulse * n)) / second.moment_area

    # Ovde cemo za svaki shape uraditi odbijanje od ivice
    @staticmethod
    def resolve_border_collision(polygon):
        result = check_border(polygon)
        if result is None:
            return
        n = result[1]
        collision_point = result[0]
        e = 1

        r_ap = collision_point - polygon.centroid
        r_ap_perpendicular = np.array([-r_ap[1], r_ap[0]])  # OVE DVE PROMENLJIVE
        invm_a = 1. / polygon.mass
        invm_b = 0.
        velocity_a = polygon.translational_speed
        velocity = velocity_a

        if np.dot(velocity, n) > 0:
            return

        incercy_a = np.power(np.dot(r_ap_perpendicular, n), 2) / polygon.moment_area
        impulse_numerator = -(1. + e) * np.dot(velocity, n)
        impulse_denominator = ((invm_a + invm_b) * np.dot(n, n)) + incercy_a
        impulse = impulse_numerator / impulse_denominator

        polygon.translational_speed = polygon.translational_speed + invm_a * impulse * n

        # impulse_denominator = ((invm_a + invm_b) * np.dot(n, n)) + incercy_a
        # impulse = impulse_numerator / impulse_denominator

        polygon.rotational_speed += -np.dot(r_ap_perpendicular, (impulse * n)) / polygon.moment_area


def text_to_screen(screen, text, x, y, size=10, color=(200, 000, 000)):
    try:
        text = str(text)
        font = pygame.font.SysFont('Comic Sans MS', size)
        text = font.render(text, True, color)
        screen.blit(text, (x, y))

    except Exception, e:
        print 'Font Error, saw it coming'
        raise e
