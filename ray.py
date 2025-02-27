import math

import pygame

from hyper_parameters import BASE_SIZE, W_SHIFT, H_SHIFT


class Ray:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.length = 0
        self.bumpedType = Ray

    def draw(self, screen, camera):
        end_x = self.x + self.length * math.cos(self.angle)
        end_y = self.y + self.length * math.sin(self.angle)

        pygame.draw.line(screen, pygame.Color('white'),
                         (W_SHIFT + (self.x - camera.x) * BASE_SIZE, H_SHIFT + (self.y - camera.y) * BASE_SIZE),
                         (W_SHIFT + (end_x - camera.x) * BASE_SIZE, H_SHIFT + (end_y - camera.y) * BASE_SIZE),
                          int(BASE_SIZE / 5))