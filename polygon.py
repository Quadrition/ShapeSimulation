import pygame
import numpy as np
from runge_kutta import runge_kutta_4



class Polygon():
    FORCE = np.array([0, 0])
    C = 3

    def __init__(self, centroid, radius, degree, mass, color=(255, 0, 0)):
        self.centroid = centroid
        self.radius = radius
        self.degree = degree
        self.mass = mass
        self.color = color
        self.reference_vector = np.array([0, -self.radius])
        self.speed = np.array([0, 0])
        self.time = pygame.time.get_ticks()
        self.angles = np.array([0, 0])

    @staticmethod
    def rotate_vector(self, vector, radians):
        return vector * np.matrix([[np.cos(radians), -np.sin(radians)], [np.sin(radians), np.cos(radians)]])

    @property
    def get_vertices(self):
        theta = -2 * np.pi / self.degree
        reference_vector = self.reference_vector
        vertices = [tuple((self.centroid + reference_vector).tolist())]
        for i in range(1, self.degree):
            reference_vector = self.rotate_vector(reference_vector, theta)
            vertices.append(tuple((self.centroid + reference_vector).tolist()))
        return vertices

    def draw(self, win):
        pygame.draw.polygon(win, self.color, self.get_vertices)

    def fun(self, t, y):
        return np.array([y[1], (self.FORCE - self.C * y[1])])

    def rotate(self, radians):
        self.reference_vector = self.rotate_vector(self.reference_vector, radians)

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
