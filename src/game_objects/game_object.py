import pygame

from src.utils.hyper_parameters import WHITE

class GameObject:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.is_destroyed = False

    def destroy(self):
        self.is_destroyed = True

    def update(self, items):
        pass

    def draw(self, screen, camera):
        pygame.draw.rect(screen, WHITE, pygame.Rect(camera.apply(self)))
