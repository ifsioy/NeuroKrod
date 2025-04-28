
import pygame

from src.game_objects.game_object import GameObject
from src.utils.hyper_parameters import YELLOW


class Key(GameObject):
    def __init__(self, x, y, width, height):
        super(Key, self).__init__(x, y, width, height)
        self.is_destroyed = False

    def draw(self, screen, camera):
        pygame.draw.rect(screen, YELLOW, pygame.Rect(camera.apply(self)))

