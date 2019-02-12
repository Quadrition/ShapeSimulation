import numpy as np
import pygame
import globals
from runge_kutta import runge_kutta_4


class Circle:

    def __init__(self, centroid, radius, mass, color=(255, 0, 0)):
        # Basic attributes
        self.centroid = centroid
        self.radius = radius
        self.reference_vector = np.array([0, -radius])
        self.color = color
        self.time = pygame.time.get_ticks()

        # Physics
        self.mass = mass

        # Translation
        self.translational_forces = np.array([np.array([0., 0.])])
        self.translational_speed = np.array([0., 0.])
        # Rotation
        self.rotational_speed = 0.
        self.moment_area = (np.pi / 4) * np.power(self.radius, 4)  # jer je 2D telo, pa nema masu, korisceno za krug, jer poligon kako raste stepen, tezi krugu

    def draw(self, win):
        pygame.draw.circle(win, self.color, np.round(self.centroid).astype(int), self.radius)

    # Calculates how much the polygon should move (translation)(
    def movement_function(self, t, y):
        force = np.array([0, 0])
        for f in self.translational_forces:
            force = force + f
        return np.array([y[1], (force - globals.FRICTION * y[1]) / self.mass])

    def move(self, dt):
        start_position = np.array([self.centroid, self.translational_speed])
        t = self.time * 0.001 + dt * 0.001
        y = runge_kutta_4(self.movement_function, dt * 0.001, start_position, self.time * 0.001)
        self.time = t
        self.centroid = y[0]
        self.translational_speed = y[1]
        self.clear_forces()

    def clear_forces(self):
        #self.forces = np.delete(self.forces, np.s_[2::], axis = 0)
        self.translational_forces = np.delete(self.translational_forces, np.s_[1::], axis = 0)

    def update(self, dt):
        self.move(dt)

    @property
    def borders(self):
        return self.centroid[0] + self.radius, self.centroid[0] - self.radius, self.centroid[1] + self.radius, \
               self.centroid[1] - self.radius
