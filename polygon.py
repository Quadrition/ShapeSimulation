from vector import Vector
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
        self.reference_vertex = Vector(0, -radius)
        self.color = color
        self.speed = np.array([0, 0])
        self.time = pygame.time.get_ticks()
        self.angles = np.array([0, 0]);

    def get_vertices(self):
        radians = 2 * math.pi / self.degree
        vertices = [(Vector(self.centroid[0], self.centroid[1]) + self.reference_vertex).get_tuple()]
        for i in range(1, self.degree):
            self.reference_vertex = self.reference_vertex.rotate(radians)
            vertices.append((Vector(self.centroid[0], self.centroid[1]) + self.reference_vertex).get_tuple())
        return vertices

    def rotate(self, radians):
        self.reference_vertex = self.reference_vertex.rotate(radians)

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
