import pygame

from game_object import GameObject
from hyper_parameters import PURPLE, KEYS_NUMBER
from player import Player


class Gates(GameObject):
    def __init__(self, x, y, width, height):
        super(Gates, self).__init__(x, y, width, height)
        self.opened = False

    def collision_check(self, another):
        if not self.collides(another):
            return False

        if type(another) == Player and another.keys_collected == KEYS_NUMBER:
            print('AND NOW, THE END IS NEAR')
        return True

    def draw(self, screen, camera):
        pygame.draw.rect(screen, PURPLE, pygame.Rect(camera.apply(self)))