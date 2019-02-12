import pygame
import globals


class Inputs:
    def __init__(self):
        self.movement_keys = [False, False, False, False]  # up right down left
        self.mouse_pos = None
        self.mouse_button = [False, False]  # left click, right click
        self.clear = False

    def is_up(self):
        return self.movement_keys[0]

    def is_right(self):
        return self.movement_keys[1]

    def is_clear(self):
        return self.clear

    def is_down(self):
        return self.movement_keys[2]

    def is_left(self):
        return self.movement_keys[3]

    def mouse_left_click(self):
        return self.mouse_button[0]

    def mouse_right_click(self):
        return self.mouse_button[1]

    def update(self):
        self.mouse_button = [False, False]
        self.clear = False
        for event in pygame.event.get():
            # Quit app
            if event.type == pygame.QUIT:
                globals.RUN = False
            # Key pressed
            elif event.type == pygame.KEYDOWN:
                # Up
                if event.key == pygame.K_UP:
                    self.movement_keys[0] = True
                # Right
                if event.key == pygame.K_RIGHT:
                    self.movement_keys[1] = True
                # Down
                if event.key == pygame.K_DOWN:
                    self.movement_keys[2] = True
                # Left
                if event.key == pygame.K_LEFT:
                    self.movement_keys[3] = True
                if event.key == pygame.K_c:
                    self.clear = True
            # Key released
            if event.type == pygame.KEYUP:
                # UP
                if event.key == pygame.K_UP:
                    self.movement_keys[0] = False
                # RIGHT
                if event.key == pygame.K_RIGHT:
                    self.movement_keys[1] = False
                # DOWN
                if event.key == pygame.K_DOWN:
                    self.movement_keys[2] = False
                # LEFT
                if event.key == pygame.K_LEFT:
                    self.movement_keys[3] = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_pos = pygame.mouse.get_pos()
                self.mouse_button = [bool(pygame.mouse.get_pressed()[0]), bool(pygame.mouse.get_pressed()[2])]
