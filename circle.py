import numpy as np
import pygame


class Circle:

    def __init__(self, centroid, radius, mass, color=(255, 0, 0)):
        self.centroid = centroid
        self.radius = radius
        self.mass = mass
        self.color = color

    def draw(self, win):
        pygame.draw.circle(win, self.color, np.round(self.centroid).astype(int), self.radius)
