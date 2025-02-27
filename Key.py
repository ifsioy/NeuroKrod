
import pygame

from Player import Player
from GameObject import GameObject
from HyperParameters import YELLOW


class Key(GameObject):
    def __init__(self, x, y, width, height):
        super(Key, self).__init__(x, y, width, height)
        self.collected = False

    def collision_check(self, another):
        if not self.collides(another):
            return False

        if type(another) == Player:
            self.collected = True
        return True

    def update(self, screen, camera, items):
        self.draw(screen, camera)


    def draw(self, screen, camera):
        pygame.draw.rect(screen, YELLOW, pygame.Rect(camera.apply(self)))

