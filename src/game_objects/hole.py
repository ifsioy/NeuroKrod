import pygame

from src.game_objects.game_object import GameObject
from src.utils.hyper_parameters import BROWN


class Hole(GameObject):
    def __init__(self, x, y, width, height):
        super(Hole, self).__init__(x, y, width, height)
        self.is_destroyed = False

    def draw(self, screen, camera):
        pygame.draw.rect(screen, BROWN, pygame.Rect(camera.apply(self)))

