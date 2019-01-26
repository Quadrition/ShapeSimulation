import numpy as np
import pygame


class Circle:

    def __init__(self, centroid, radius, mass, color=(255, 0, 0)):
        self.centroid = centroid
        self.radius = radius
        self.mass = mass
        self.color = color
        self.speed = np.array([0, 0])
        self.time = pygame.time.get_ticks()
        self.angles = np.array([0, 0])
        self.forces = np.array([np.array([0., 0.]), np.array([0., 0.])])

    def draw(self, win):
        pygame.draw.circle(win, self.color, self.centroid, self.radius)
