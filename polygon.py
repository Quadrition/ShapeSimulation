import math
import pygame
import numpy as np
from runge_kutta import runge_kutta_4


class Polygon():
    FORCE = np.array([0, 0])
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

    def rotate_reference_vector(self, theta):
        self.reference_vector = self.reference_vector * np.matrix(
            [[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])

    @property
    def theta(self):
        return 2 * math.pi / self.degree

    def get_vertices(self):
        theta = self.theta
        vertices = [tuple((self.centroid + self.reference_vector).tolist())]
        for i in range(1, self.degree):
            self.rotate_reference_vector(theta)
            vertices.append(tuple((self.centroid + self.reference_vector).tolist()))
        self.rotate_reference_vector(theta)
        return vertices

    def rotate(self, theta):
        self.reference_vector = self.reference_vector * np.matrix(
            [[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])

    def draw(self, win):
        pygame.draw.polygon(win, self.color, self.get_vertices())

    def fun(self, t, y):
        return np.array([y[1], (self.FORCE - self.C * y[1])])

    def move(self, dt):
        self.start = np.array([self.centroid, self.speed])
        t = self.time * 0.001 + dt * 0.001
        y = runge_kutta_4(self.fun, dt * 0.001, self.start, self.time * 0.001)
        self.time = t
        self.start = y
        self.centroid = y[0]
        self.speed = y[1]
        print self.centroid, self.speed

    def update(self, dt):
        self.move(dt)
        self.rotate(2 * math.pi * dt * 0.001)
