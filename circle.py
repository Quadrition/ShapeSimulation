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
        self.forces = np.array([np.array([0., 0.]), 0.])
        self.mass = mass

        # Translation
        self.translational_forces = np.array([np.array([0., 0.])])
        self.translational_speed = np.array([0., 0.])
        # Rotation
        self.angle = 0.
        self.torques = np.array([0.])
        self.rotational_speed = 0.
        self.moment_area = (np.pi / 4.) * self.radius  # jer je 2D telo, pa nema masu, korisceno za krug, jer poligon kako raste stepen, tezi krugu

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
        start_angle = np.array([self.angle, self.rotational_speed])
        t = self.time * 0.001 + dt * 0.001
        y = runge_kutta_4(self.movement_function, dt * 0.001, start_position, self.time * 0.001)
        self.time = t
        # start_position = y
        # start_angle = theta_p
        self.centroid = y[0]
        self.translational_speed = y[1]
        #print self.rotational_speed
        self.clear_forces()

    def clear_forces(self):
        #self.forces = np.delete(self.forces, np.s_[2::], axis = 0)
        self.torques = np.array([0.])
        self.translational_forces = np.delete(self.translational_forces, np.s_[1::], axis = 0)
        self.forces = np.array([np.array([0., 0.]), 0.])

    def update(self, dt):
        self.move(dt)
