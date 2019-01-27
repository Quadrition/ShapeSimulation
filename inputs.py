import pygame
import globals

class Inputs:
    def __init__(self):
        self.movement_keys = [False, False, False, False] # left up right down
        self.rotate_keys = [False, False]

    def get_left(self):
        return self.movement_keys[0]

    def get_right(self):
        return self.movement_keys[2]

    def get_down(self):
        return self.movement_keys[3]

    def get_up(self):
        return self.movement_keys[1]

    def get_cw(self):
        return self.rotate_keys[0]

    def update(self):
        for event in pygame.event.get():
            # QUIT
            if event.type == pygame.QUIT:
                globals.RUN = False
            elif event.type == pygame.KEYDOWN:
                # LEFT
                if event.key == pygame.K_LEFT and self.movement_keys[0] == False :
                    self.movement_keys[0] = True
                # UP
                if event.key == pygame.K_UP and self.movement_keys[1] == False :
                    self.movement_keys[1] = True
                # RIGHT
                if event.key == pygame.K_RIGHT and self.movement_keys[2] == False :
                    self.movement_keys[2] = True
                # DOWN
                if event.key == pygame.K_DOWN and self.movement_keys[3] == False :
                    self.movement_keys[3] = True
                # ROTATE CW
                if event.key == pygame.K_k and self.rotate_keys[0] == False:
                    self.rotate_keys[0] = True

            if event.type == pygame.KEYUP:
                # LEFT
                if event.key == pygame.K_LEFT and self.movement_keys[0] == True:
                    self.movement_keys[0] = False
                if event.key == pygame.K_UP and self.movement_keys[1] == True:
                    self.movement_keys[1] = False
                if event.key == pygame.K_RIGHT and self.movement_keys[2] == True:
                    self.movement_keys[2] = False
                if event.key == pygame.K_DOWN and self.movement_keys[3] == True:
                    self.movement_keys[3] = False
                # ROTATE CW
                if event.key == pygame.K_k and self.rotate_keys[0] == True:
                    self.rotate_keys[0] = False
