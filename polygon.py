import math
import pygame
import numpy as np
from runge_kutta import runge_kutta_4
from projection import Projection


class Polygon:
    C = 3

    def __init__(self, centroid, radius, degree, mass, color=(255, 0, 0)):
        self.centroid = centroid
        self.degree = degree
        self.mass = mass
        self.reference_vector = np.array([0, -radius])
        self.color = color
        self.speed = np.array([0, 0])
        self.time = pygame.time.get_ticks()
        self.angles = np.array([0, 0])
        self.forces = np.array([np.array([0., 0.]), np.array([0., 0.])])

    def rotate_reference_vector(self, theta):
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
            self.rotate_reference_vector(theta)
            vertices.append(self.centroid + self.reference_vector)
        self.rotate_reference_vector(theta)
        return vertices

    def rotate(self, theta):
        self.reference_vector = self.reference_vector * np.matrix(
            [[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])

    def draw(self, win):
        vertices = self.vertices
        for i in range(len(vertices)):
            vertices[i] = tuple(vertices[i].tolist())
        pygame.draw.polygon(win, self.color, vertices)

    def fun(self, t, y):
        force = np.array([0, 0])
        for f in self.forces:
            force = force + f
        return np.array([y[1], (force - self.C * y[1]) / self.mass])

    def move(self, dt):
        self.start = np.array([self.centroid, self.speed])
        t = self.time * 0.001 + dt * 0.001
        y = runge_kutta_4(self.fun, dt * 0.001, self.start, self.time * 0.001)
        self.time = t
        self.start = y
        self.centroid = y[0]
        self.speed = y[1]
        # print self.forces

    def update(self, dt):
        self.move(dt)
        # self.rotate(2 * math.pi * dt * 0.005)
