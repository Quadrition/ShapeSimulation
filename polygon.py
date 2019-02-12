import math
import pygame
import numpy as np
from runge_kutta import runge_kutta_4
import globals


class Polygon:

    def __init__(self, centroid, radius, degree, mass, color=(255, 0, 0)):
        # Basic attributes
        self.centroid = centroid
        self.degree = degree
        self.radius = radius
        self.reference_vector = np.array([0, -radius])
        self.color = color
        self.time = pygame.time.get_ticks()

        # Physics

        # self.mass = density * self.area
        self.mass = mass  # density * self.area * math.pow(10, -5)#[kg] = [g/cm^2] * [mm^2]
        # Translation
        self.translational_forces = []
        self.translational_speed = np.array([0., 0.])
        # Rotation
        self.angle = 0.
        self.torques = np.array([0.])
        self.rotational_speed = 0.
        self.moment_area = math.pow(radius, 4) * np.pi / 400

    def rotate(self, theta):
        self.reference_vector = np.array(self.reference_vector * np.matrix(
            [[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])).ravel()

    @property
    def theta(self):
        return 2 * math.pi / self.degree

    @property
    def vertices(self):
        theta = self.theta
        vertices = [self.centroid + self.reference_vector]
        for i in range(1, self.degree):
            self.rotate(theta)
            vertices.append(self.centroid + self.reference_vector)
        self.rotate(theta)
        return vertices

    def draw(self, win):
        vertices = self.vertices
        for i in range(len(vertices)):
            vertices[i] = tuple(vertices[i].tolist())
        pygame.draw.polygon(win, self.color, vertices)

    # Calculates how much the polygon should move (translation)(
    def movement_function(self, t, y):
        force = np.array([0, 0])
        for f in self.translational_forces:
            force = force + f
        return np.array([y[1], (force - globals.FRICTION * y[1]) / self.mass])

    # Calculates how much the polygon should rotate
    def rotation_function(self, t, y):
        torque = 0.
        for f in self.torques:
            torque = torque + f
        return np.array([y[1], (torque - globals.ROTATION_FRICTION * y[1]) / self.moment_area])

    # Adds a force acting on the polygon and calculates torque and translational force
    def add_force(self, force):
        self.translational_forces.append(force)

    # Clears all forces acting on the polygon
    def clear_forces(self):
        #self.forces = np.delete(self.forces, np.s_[2::], axis = 0)
        self.torques = np.array([0.])
        self.translational_forces = []
        #self.forces = np.array([np.array([0., 0.]), 0.])

    def move(self, dt):
        start_position = np.array([self.centroid, self.translational_speed])
        start_angle = np.array([self.angle, self.rotational_speed])
        t = self.time * 0.001 + dt * 0.001
        y = runge_kutta_4(self.movement_function, dt * 0.001, start_position, self.time * 0.001)
        theta_p = runge_kutta_4(self.rotation_function, dt * 0.001, start_angle, self.time * 0.001)
        self.time = t
        self.centroid = y[0]
        self.translational_speed = y[1]
        self.rotate(theta_p[0] - self.angle)
        self.angle = theta_p[0]
        self.rotational_speed = theta_p[1]
        self.clear_forces()

    def update(self, dt):
        self.move(dt)

    @property
    def borders(self):
        x_max = -float('inf')
        x_min = float('inf')
        y_max = -float('inf')
        y_min = float('inf')
        for vertex in self.vertices:
            if vertex[0] < x_min:
                x_min = vertex[0]
            if vertex[0] > x_max:
                x_max = vertex[0]
            if vertex[1] < y_min:
                y_min = vertex[1]
            if vertex[1] > y_max:
                y_max = vertex[1]
        return x_max, x_min, y_max, y_min
